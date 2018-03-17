# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from requests import get

from spbu.consts import main_url, available_lessons_types
from spbu.types import ApiException


def get_group_events(group_id, from_date=None, to_date=None,
                     lessons_type="Unknown", timeout=5):
    """
    Gets a given student group's events for the current week or
    Gets a given student group's events for a week starting from a specified
        datetime until the end of the week or
    Gets events for a specified date range.
    :param group_id: The student group's id.
    :type group_id: int
    :param from_date: (Optional) The datetime the events start from.
    :type from_date: date
    :param to_date: (Optional) The datetime the events ends. Use only with
                    `from_date`.
    :type to_date: date
    :param lessons_type: (Optional) The type of lessons type.
    :type lessons_type: str
    :param timeout: (Optional) request timeout in seconds
    :type timeout: int
    :return: The result parsed to a JSON dictionary.
    :rtype: dict
    :raises spbu.ApiException: if `response status code` is not 200.
    :raises requests.exceptions.ReadTimeout: if the request exceeds the timeout.
    """
    sub_url = "groups/{0}/events"
    params = {}

    if lessons_type in available_lessons_types:
        params["timetable"] = lessons_type

    if from_date and to_date:
        sub_url += "/{0}/{1}".format(from_date, to_date)
    elif from_date:
        sub_url += "/{0}".format(from_date)

    result = get(url=main_url + sub_url.format(group_id, from_date, to_date),
                 params=params,
                 timeout=timeout)

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Get extracur events", result)

    return result.json()
