# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from requests import get

from spbu.apiexception import ApiException
from spbu.consts import main_url


def get_extracur_divisions():
    """
    Gets extracurricular divisions.
    :return: The result parsed to a JSON dictionary.
    :rtype: list
    :raises ApiException: if `response status code` is not 200.
    """
    sub_url = "extracur/divisions"

    result = get(url=main_url + sub_url)

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Get extracur divisions", result)

    return result.json()


def get_extracur_events(alias, from_date=None):
    """
    Get extracurricular events for a given division.
    :param alias: The division's short name code (alias).
    :type alias: str
    :param from_date: (Optional) The date the events start from.
    :type from_date: date
    :return: The result parsed to a JSON dictionary.
    :rtype: dict
    :raises ApiException: if `response status code` is not 200.
    """
    sub_url = "extracur/divisions/{0}/events"
    params = {}

    if from_date:
        params["fromDate"] = from_date

    result = get(url=main_url + sub_url.format(alias),
                 params=params)

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Get extracur events", result)

    return result.json()
