import datetime
import json
import csv
from json import JSONEncoder
from typing import Any, Dict, List, Union, TextIO
from sys import stdout
from enum import Enum
from tabulate import tabulate
from .user import User
from .repository import Repository


class Serializer(JSONEncoder):
    def default(self, o: Any) -> Any:
        """
        A custom cls to be used with json.loads()
        :param o: object to be converted to dict
        :return: iso formatted date string for datetime.date or datetime.datetime, o.__dict__ else
        """
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        elif isinstance(o, dict):
            return o
        else:
            return o.__dict__


class PROP(Enum):
    users = 'user_data'
    repos = 'repo_data'


class FIELD(Enum):
    user_data = User
    repo_data = Repository


def writer_wrapper(writer):
    def wrapper(ref, g: object):
        writer(ref, g)
        if ref.file_handle is stdout:
            ref.file_handle.write('\n')

    return wrapper


class Writer:
    obj: object
    prop: str
    type: str
    out_file: Union[TextIO, str] = stdout
    writers: Dict[str, callable]
    display_rows: List[str]
    __ascii_threshold = 4
    file_handle: TextIO = stdout

    def __init__(self, prop, obj, out_type, out_file=None):
        self.obj = obj
        self.prop = prop
        self.type = out_type
        self.display_rows = FIELD[prop].value.display_rows
        self.writers = {
            'json': self.__to_json,
            'csv': self.__to_csv,
            'ascii': self.__to_ascii_table,
            'html': self.__to_html_table
        }
        if out_file is not None:
            self.out_file = out_file
            self.file_handle = open(out_file, 'w')

    def __del__(self):
        if self.file_handle is not stdout:
            self.file_handle.close()

    def write(self):
        writer = self.__get_writer()
        attr = getattr(self.obj, self.prop)
        writer(attr)

    def __get_writer(self):
        return self.writers[self.type]

    @writer_wrapper
    def __to_json(self, g: object):
        json.dump(g, self.file_handle, cls=Serializer, indent=4, sort_keys=True)

    @writer_wrapper
    def __to_csv(self, g: object):
        dict_obj = Writer.__to_dict(g)
        headers = Writer.__get_headers(dict_obj)
        writer = csv.DictWriter(self.file_handle, fieldnames=headers)
        writer.writeheader()
        for entry in dict_obj.keys():
            writer.writerow(dict_obj[entry])

    @writer_wrapper
    def __to_ascii_table(self, g: Dict[str, Union[User, Repository]]):
        headers, rows = Writer.__get_table_content(g)
        if len(g.keys()) < Writer.__ascii_threshold:
            table_writer = self.__get_table_transpose(g, headers, rows)
        else:
            table_writer = self.__get_table(headers, rows)
        self.file_handle.write(table_writer)

    @writer_wrapper
    def __to_html_table(self, g: Dict[str, Union[User, Repository]]):
        headers, rows = self.__get_table_content(g)
        table_writer = tabulate(rows, headers=headers, tablefmt='html')
        self.file_handle.write(table_writer)

    @staticmethod
    def __to_dict(g: object) -> Dict[str, Any]:
        return json.loads(json.dumps(g, cls=Serializer, indent=4, sort_keys=True))

    @staticmethod
    def __get_headers(g: Dict[str, Any]) -> List[str]:
        members = list(g.keys())
        return list(g[members[0]].keys())

    @staticmethod
    def __get_table_transpose(g: Dict[str, Union[User, Repository]], headers: List[str], rows: List[str]):
        new_headers, new_rows = Writer.__get_transpose(g, rows, headers)
        return tabulate(new_rows, headers=new_headers, tablefmt='pretty')

    @staticmethod
    def __get_table(headers: List[str], rows: List[str]):
        return tabulate(rows, headers=headers, tablefmt='plain')

    @staticmethod
    def __get_table_content(g: Dict[str, Union[User, Repository]]):
        dict_repr = Writer.__to_dict(g)
        headers = Writer.__get_headers(dict_repr)
        rows = Writer.__get_entries_as_rows(dict_repr)
        return headers, rows

    @staticmethod
    def __get_entries_as_rows(g: Dict[str, Any]) -> List[Any]:
        rows = []
        for entry in g.keys():
            rows.append(list(g[entry].values()))
        return rows

    @staticmethod
    def __get_transpose(g: Dict[str, Union[User, Repository]], rows, headers):
        new_rows = []
        new_headers = [' '] + list(g.keys())
        for i in range(len(rows[0])):
            new_rows.append([rows[j][i] for j in range(len(rows))])
        for i in range(len(new_rows)):
            new_rows[i] = [headers[i]] + new_rows[i]
        return new_headers, new_rows
