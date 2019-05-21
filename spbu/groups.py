from datetime import date

from . import util
from .consts import LessonsTypes, APIMethods
from .types import GroupEvents


def get_group_events(group_id: int, from_date: date = None,
                     to_date: date = None,
                     lessons_type: LessonsTypes = LessonsTypes.UNKNOWN) -> GroupEvents:
    if from_date and to_date:
        method = APIMethods.G_EVENTS_FROM_TO
        path_values = {
            "id": group_id,
            "from": from_date,
            "to": to_date
        }
    elif from_date:
        method = APIMethods.G_EVENTS_FROM
        path_values = {
            "id": group_id,
            "from": from_date
        }
    else:
        method = APIMethods.G_EVENTS
        path_values = {
            "id": group_id
        }
    return GroupEvents.de_json(
        util.call_api(
            method=method,
            path_values=path_values,
            params={
                "timetable": lessons_type.value
            }
        )
    )
