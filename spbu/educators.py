from datetime import date
from typing import List

from . import util
from .consts import APIMethods, LessonsTypes
from .types import EducatorEventsTerm, Educator, EducatorEvents


def get_educator_term_events(educator_id: int,
                             next_term: bool = False) -> EducatorEventsTerm:
    return EducatorEventsTerm.de_json(
        util.call_api(
            method=APIMethods.E_EVENTS,
            path_values={
                "id": educator_id
            },
            params={
                "showNextTerm": int(next_term)
            }
        )
    )


def get_educator_events(educator_id: int, _from: date, _to: date,
                        lessons_type: LessonsTypes = LessonsTypes.UNKNOWN) -> EducatorEvents:
    return EducatorEvents.de_json(
        util.call_api(
            method=APIMethods.E_EVENTS_FROM_TO,
            path_values={
                "id": educator_id,
                "from": _from,
                "to": _to
            },
            params={
                "timetable": lessons_type.value
            }
        )
    )


def search_educator(query: str) -> List[Educator]:
    return [
        Educator.de_json(ed)
        for ed in util.call_api(
            method=APIMethods.E_SEARCH,
            path_values={
                "query": query
            }
        )["Educators"]
    ]
