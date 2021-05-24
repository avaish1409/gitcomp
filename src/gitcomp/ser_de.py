import datetime
import json
from json import JSONEncoder
from typing import Any, Dict
from sys import stdout


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


def to_json(g: object, dest):
    file_handle = dest
    if dest is not stdout:
        file_handle = open(dest, 'w')
    json.dump(g, file_handle, cls=Serializer, indent=4, sort_keys=True)


def to_dict(g: object) -> Dict[str, str]:
    return json.loads(json.dumps(g, cls=Serializer, indent=4, sort_keys=True))


WRITERS = {
    'json': to_json
}


class Writer:
    obj: object
    prop: str
    type: str
    out_file: Any = stdout

    def __init__(self, prop, obj, tp, out_file):
        self.obj = obj
        self.prop = prop
        self.type = tp
        if out_file is not None:
            self.out_file = out_file

    def __get_writer(self):
        return WRITERS[self.type]

    def write(self):
        writer = self.__get_writer()
        attr = getattr(self.obj, self.prop)
        writer(attr, self.out_file)
