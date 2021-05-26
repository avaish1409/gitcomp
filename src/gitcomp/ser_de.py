import datetime
import json
import csv
from json import JSONEncoder
from typing import Any, Dict, List
from sys import stdout
from prettytable import PrettyTable


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

    def __init__(self, prop, obj, tp, out_file):
        self.obj = obj
        self.prop = prop
        self.type = tp
        self.writers = {
            'json': self.to_json,
            'csv': self.to_csv,
            'ascii': self.to_ascii_table
        }
        if out_file is not None:
            self.out_file = out_file

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

    @staticmethod
    def get_entries_as_rows(g: Dict[str, Any]) -> List[Any]:
        rows = []
        for entry in g.keys():
            rows.append(list(g[entry].values()))
        return rows

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

    def to_ascii_table(self, g: object):
        file_handle = self.get_file_handle()
        dict_repr = Writer.to_dict(g)
        headers = Writer.get_headers(dict_repr)
        rows = Writer.get_entries_as_rows(dict_repr)
        table_writer = PrettyTable()
        table_writer.field_names = headers
        table_writer.add_rows(rows)
        file_handle.write(table_writer.get_string())
        Writer.close_file_handle(file_handle)

    def __get_writer(self):
        return self.writers[self.type]

    def write(self):
        writer = self.__get_writer()
        attr = getattr(self.obj, self.prop)
        writer(attr)
