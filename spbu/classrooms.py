from datetime import datetime

from . import util
from .consts import APIMethods
from .types import ClassroomBusyness, ClassroomEvents


def _create_string_from_datetime(dt: datetime) -> str:
    return dt.strftime("%Y%m%d%H%M")


def is_classroom_busy(oid: str, start: datetime,
                      end: datetime) -> ClassroomBusyness:
    return ClassroomBusyness.de_json(
        util.call_api(
            method=APIMethods.C_IS_BUSY,
            path_values={
                "oid": oid,
                "start": _create_string_from_datetime(start),
                "end": _create_string_from_datetime(end)
            }
        )
    )


def get_classroom_events(oid: str, _from: datetime,
                         _to: datetime) -> ClassroomEvents:
    return ClassroomEvents.de_json(
        util.call_api(
            method=APIMethods.C_EVENTS,
            path_values={
                "oid": oid,
                "from": _create_string_from_datetime(_from),
                "to": _create_string_from_datetime(_to)
            }
        )
    )
