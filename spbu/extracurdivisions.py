from datetime import date
from typing import List

from .consts import APIMethods
from .types import ExtracurDivision, ExtracurEvents
from . import util


def get_extracur_divisions() -> List[ExtracurDivision]:
    return [
        ExtracurDivision.de_json(ex_div)
        for ex_div in util.call_api(
            method=APIMethods.ED_DIVISIONS
        )
    ]


def get_extracur_events(alias: str, from_date: date = None) -> ExtracurEvents:
    return ExtracurEvents.de_json(
        util.call_api(
            method=APIMethods.ED_EVENTS,
            path_values={
                "alias": alias
            },
            params={
                "fromDate": from_date
            } if from_date else {}
        )
    )
