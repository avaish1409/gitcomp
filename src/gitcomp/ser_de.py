import datetime
import json
import csv
from json import JSONEncoder
from typing import Any, Dict, List, Union
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


class Writer:
    obj: object
    prop: str
    type: str
    out_file: Any = stdout
    writers: Dict[str, callable]
    display_rows: List[str]
    __ascii_threshold = 4

    def __init__(self, prop, obj, out_type, out_file):
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

    def write(self):
        writer = self.__get_writer()
        attr = getattr(self.obj, self.prop)
        writer(attr)

    def __get_writer(self):
        return self.writers[self.type]

    def __to_json(self, g: object):
        file_handle = self.__get_file_handle()
        json.dump(g, file_handle, cls=Serializer, indent=4, sort_keys=True)
        self.__close_file_handle(file_handle)

    def __to_csv(self, g: object):
        file_handle = self.__get_file_handle()
        dict_obj = Writer.__to_dict(g)
        headers = Writer.__get_headers(dict_obj)
        writer = csv.DictWriter(file_handle, fieldnames=headers)
        writer.writeheader()
        for entry in dict_obj.keys():
            writer.writerow(dict_obj[entry])
        Writer.__close_file_handle(file_handle)

    def __to_ascii_table(self, g: Dict[str, Union[User, Repository]]):
        file_handle = self.__get_file_handle()
        if len(g.keys()) < Writer.__ascii_threshold:
            table_writer = self.__get_table_transpose(g)
        else:
            table_writer = self.__get_table(g)
        file_handle.write(table_writer)
        Writer.__close_file_handle(file_handle)

    def __to_html_table(self, g: Dict[str, Union[User, Repository]]):
        file_handle = self.__get_file_handle()
        table_writer = self.__get_table(g)
        table_writer.format = True
        file_handle.write(table_writer.get_html_string(fields=self.display_rows))
        Writer.__close_file_handle(file_handle)

    def __get_file_handle(self):
        if self.out_file is not stdout:
            return open(self.out_file, 'w')
        return self.out_file

    @staticmethod
    def __close_file_handle(handle):
        if handle is not stdout:
            handle.close()

    @staticmethod
    def __to_dict(g: object) -> Dict[str, Any]:
        return json.loads(json.dumps(g, cls=Serializer, indent=4, sort_keys=True))

    @staticmethod
    def __get_headers(g: Dict[str, Any]) -> List[str]:
        members = list(g.keys())
        return list(g[members[0]].keys())

    @staticmethod
    def __get_table_transpose(g: Dict[str, Union[User, Repository]]):
        dict_repr = Writer.__to_dict(g)
        headers = Writer.__get_headers(dict_repr)
        rows = Writer.__get_entries_as_rows(dict_repr)
        new_headers, new_rows = Writer.__get_transpose(g, rows, headers)
        return tabulate(new_rows, headers=new_headers, tablefmt='pretty')

    @staticmethod
    def __get_table(g: Dict[str, Union[User, Repository]]):
        dict_repr = Writer.__to_dict(g)
        headers = Writer.__get_headers(dict_repr)
        rows = Writer.__get_entries_as_rows(dict_repr)
        return tabulate(rows, headers=headers, tablefmt='plain')

    @staticmethod
    def __get_entries_as_rows(g: Dict[str, Any]) -> List[Any]:
        rows = []
        for entry in g.keys():
            rows.append(list(g[entry].values()))
        return rows

    @staticmethod
    def __get_transpose(g: Dict[str, Union[User, Repository]], rows, headers):
        new_rows = []
        new_headers = ['Argument'] + list(g.keys())
        for i in range(len(rows[0])):
            new_rows.append([rows[j][i] for j in range(len(rows))])
        for i in range(len(new_rows)):
            new_rows[i] = [headers[i]] + new_rows[i]
        return new_headers, new_rows
