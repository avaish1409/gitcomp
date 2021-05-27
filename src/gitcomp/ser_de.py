import datetime
import json
import csv
from json import JSONEncoder
from typing import Any, Dict, List, Union
from sys import stdout
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


class Writer:
    obj: object
    prop: str
    type: str
    out_file: Any = stdout
    writers: Dict[str, callable]
    display_rows: List[str]
    prop_map: Dict[str, Union[User, Repository]] = {
        'user_data': User,
        'repo_data': Repository
    }

    def __init__(self, prop, obj, tp, out_file):
        self.obj = obj
        self.prop = prop
        self.type = tp
        self.writers = {
            'json': self.to_json,
            'csv': self.to_csv,
            'ascii': self.to_ascii_table,
            'html': self.to_html_table
        }
        if out_file is not None:
            self.out_file = out_file
        self.display_rows = Writer.prop_map[prop].display_rows

    @staticmethod
    def close_file_handle(handle):
        if handle is not stdout:
            handle.close()

    @staticmethod
    def to_dict(g: object) -> Dict[str, Any]:
        return json.loads(json.dumps(g, cls=Serializer, indent=4, sort_keys=True))

    @staticmethod
    def get_headers(g: Dict[str, Any]) -> List[str]:
        members = list(g.keys())
        return list(g[members[0]].keys())

    def get_file_handle(self):
        if self.out_file is not stdout:
            return open(self.out_file, 'w')
        return self.out_file

    def to_json(self, g: object):
        file_handle = self.get_file_handle()
        json.dump(g, file_handle, cls=Serializer, indent=4, sort_keys=True)
        self.close_file_handle(file_handle)

    def to_csv(self, g: object):
        file_handle = self.get_file_handle()
        dict_obj = Writer.to_dict(g)
        headers = Writer.get_headers(dict_obj)
        writer = csv.DictWriter(file_handle, fieldnames=headers)
        writer.writeheader()
        for entry in dict_obj.keys():
            writer.writerow(dict_obj[entry])
        Writer.close_file_handle(file_handle)

    def __get_writer(self):
        return self.writers[self.type]

    def __get_table_headers(self) -> List[str]:
        return sorted(self.display_rows)

    def to_ascii_table(self, g: object):
        file_handle = self.get_file_handle()
        headers, rows = self.__get_table(g)
        table = tabulate(rows, headers=self.__get_table_headers(), tablefmt='plain')
        file_handle.write(table)
        Writer.close_file_handle(file_handle)

    def to_html_table(self, g: object):
        file_handle = self.get_file_handle()
        headers, rows = self.__get_table(g)
        table = tabulate(rows, headers=headers, tablefmt='html')
        file_handle.write(table)
        Writer.close_file_handle(file_handle)

    def __get_table(self, g: object):
        headers = self.__get_table_headers()
        dict_repr = Writer.to_dict(g)
        rows = Writer.get_entries_as_rows(dict_repr, headers)
        return headers, rows

    @staticmethod
    def get_entries_as_rows(g: Dict[str, Any], attrs: List[str]) -> List[List[Any]]:
        rows = []
        for entry in g.keys():
            row = []
            for field in attrs:
                row.append(g[entry][field])
            rows.append(row)
        return rows

    def write(self):
        writer = self.__get_writer()
        attr = getattr(self.obj, self.prop)
        writer(attr)
