from typing import List

from . import util
from .consts import APIMethods
from .types import PGGroup


def get_groups(program_id: int) -> List[PGGroup]:
    return [
        PGGroup.de_json(gr)
        for gr in util.call_api(
            method=APIMethods.P_GROUPS,
            path_values={
                "id": program_id
            }
        )["Groups"]
    ]
