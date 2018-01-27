# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from requests import get

from spbu.apiexception import ApiException
from spbu.consts import main_url, available_seating_types


def _create_params(seating=None, capacity=None, equipment=None):
    """
    Creates a dict `params` to use in the API request.
    :param: seating: (Optional) Seating type: theater, amphitheater, roundtable.
            Uses any seating type if not specified.
    :type seating: str
    :param: capacity: (Optional) Minimal capacity.
    :type capacity: int
    :param: equipment: (Optional) Equipment: comma-separated values list.
    :type equipment: str
    :return: The dictionary.
    :rtype: dict
    """
    params = {}
    if seating in available_seating_types:
        params["seating"] = seating

    if capacity is not None:
        params["capacity"] = capacity

    if equipment is not None:
        params["equipment"] = equipment

    return params


def get_addresses(seating=None, capacity=None, equipment=None):
    """
    Gets addresses filtered by a given optional criteria.
    :param: seating: (Optional) Seating type: theater, amphitheater, roundtable.
            Uses any seating type if not specified.
    :type seating: str
    :param: capacity: (Optional) Minimal capacity.
    :type capacity: int
    :param: equipment: (Optional) Equipment: comma-separated values list.
    :type equipment: str
    :return: The result parsed to a JSON dictionary.
    :rtype: list
    :raises: ApiException: if `response status code` is not 200.
    """
    sub_url = "addresses"
    params = _create_params(seating, capacity, equipment)

    result = get(url=main_url + sub_url,
                 params=params)

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Get addresses", result)

    return result.json()


def get_classrooms(oid, seating=None, capacity=None, equipment=None):
    """
    Gets classrooms by a given optional criteria.
    :param oid: The address id: GUID.
    :type oid: str
    :param seating: (Optional) Seating type: theater, amphitheater, roundtable.
           Uses any seating type if not specified.
    :type seating: str
    :param capacity: (Optional) Minimal capacity.
    :type capacity: int
    :param equipment: (Optional) Equipment: comma-separated values list.
    :type equipment: str
    :return: The result parsed to a JSON dictionary.
    :rtype: list
    :raises ApiException: if `response status code` is not 200.
    """
    sub_url = "addresses/{0}/classrooms"
    params = _create_params(seating, capacity, equipment)

    result = get(url=main_url + sub_url.format(oid),
                 params=params)

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Get classrooms", result)

    return result.json()
