import datetime
import json
from json import JSONEncoder
from typing import Any, Dict


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


def to_json_str(g: object) -> str:
    return json.dumps(g, cls=Serializer, indent=4, sort_keys=True)


def to_dict(g: object) -> Dict[str, str]:
    return json.loads(to_json_str(g))
