import datetime
from json import JSONEncoder
from typing import Any


class CustomJSONEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        else:
            return o.__dict__
