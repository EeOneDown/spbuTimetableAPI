from typing import List

from . import util
from .consts import APIMethods
from .types import SDStudyDivision, SDPLStudyLevel


def get_study_divisions() -> List[SDStudyDivision]:
    return [
        SDStudyDivision.de_json(sd)
        for sd in util.call_api(
            method=APIMethods.SD_DIVISIONS
        )
    ]


def get_programs(alias: str) -> List[SDPLStudyLevel]:
    return [
        SDPLStudyLevel.de_json(sl)
        for sl in util.call_api(
            method=APIMethods.SD_PROGRAMS,
            path_values={
                "alias": alias
            }
        )
    ]
