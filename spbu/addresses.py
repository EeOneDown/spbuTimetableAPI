from typing import List

from . import util
from .consts import SeatingTypes, APIMethods
from .types import Address, Classroom


def _create_params(seating: SeatingTypes = None, capacity: int = None,
                   equipment: str = None) -> dict:
    params = {}
    if seating is not None:
        params["seating"] = seating.value

    if capacity is not None:
        params["capacity"] = capacity

    if equipment is not None:
        params["equipment"] = equipment

    return params


def get_addresses(seating: SeatingTypes = None, capacity: int = None,
                  equipment: str = None) -> List[Address]:
    return [
        Address.de_json(adr)
        for adr in util.call_api(
            method=APIMethods.A_ADDRESSES,
            params=_create_params(seating, capacity, equipment)
        )
    ]


def get_classrooms(oid: str, seating: SeatingTypes = None, capacity: int = None,
                   equipment: str = None) -> List[Classroom]:
    return [
        Classroom.de_json(cls)
        for cls in util.call_api(
            method=APIMethods.A_CLASSROOMS,
            path_values={'oid': oid},
            params=_create_params(seating, capacity, equipment)
        )
    ]
