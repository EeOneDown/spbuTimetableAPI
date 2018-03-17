# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from requests import get

from spbu.consts import main_url
from spbu.types import ApiException


def get_extracur_divisions(timeout=5):
    """
    Gets extracurricular divisions.
    :param timeout: (Optional) request timeout in seconds
    :type timeout: int
    :return: The result parsed to a JSON dictionary.
    :rtype: list
    :raises spbu.ApiException: if `response status code` is not 200.
    :raises requests.exceptions.ReadTimeout: if the request exceeds the timeout.
    """
    sub_url = "extracur/divisions"

    result = get(url=main_url + sub_url,
                 timeout=timeout)

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Get extracur divisions", result)

    return result.json()


def get_extracur_events(alias, from_date=None, timeout=5):
    """
    Get extracurricular events for a given division.
    :param alias: The division's short name code (alias).
    :type alias: str
    :param from_date: (Optional) The date the events start from.
    :type from_date: date
    :param timeout: (Optional) request timeout in seconds
    :type timeout: int
    :return: The result parsed to a JSON dictionary.
    :rtype: dict
    :raises spbu.ApiException: if `response status code` is not 200.
    :raises requests.exceptions.ReadTimeout: if the request exceeds the timeout.
    """
    sub_url = "extracur/divisions/{0}/events"
    params = {}

    if from_date:
        params["fromDate"] = from_date

    result = get(url=main_url + sub_url.format(alias),
                 params=params,
                 timeout=timeout)

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Get extracur events", result)

    return result.json()
