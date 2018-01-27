# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from requests import get

from spbu.apiexception import ApiException
from spbu.consts import main_url


def _create_string_from_datetime(dt):
    """
    Creates a specific string from a datetime object.
    :param dt: A datetime object.
    :type dt: datetime
    :return: Specific sting.
    :rtype: str
    """
    return dt.strftime("%Y%m%d%H%M")


def is_classroom_busy(oid, start, end):
    """
    Checks whether a given classroom is busy in a specified interval
    or it's part.
    :param oid: The classroom's id.
    :type oid: str
    :param start: The interval's start.
    :type start: datetime
    :param end: The interval's end.
    :type end: datetime
    :return: The result parsed to a JSON dictionary.
    :rtype: dict
    :raises ApiException: if `response status code` is not 200.
    """
    sub_url = "classrooms/{0}/isbusy/{1}/{2}"
    start = _create_string_from_datetime(start)
    end = _create_string_from_datetime(end)

    result = get(url=main_url + sub_url.format(oid, start, end))

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Is classroom busy", result)

    return result.json()
