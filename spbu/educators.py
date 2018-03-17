# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from requests import get

from spbu.consts import main_url
from spbu.types import ApiException


def get_educator_events(educator_id, next_term=False, timeout=5):
    """
    Gets an educator's events for the current study term.
    :param educator_id: The educator's id.
    :type educator_id: int
    :param next_term: (Optional) Whether to show the events for the next term.
    :type next_term: bool
    :param timeout: (Optional) request timeout in seconds
    :type timeout: int
    :return: The result parsed to a JSON dictionary.
    :rtype: dict
    :raises spbu.ApiException: if `response status code` is not 200.
    :raises requests.exceptions.ReadTimeout: if the request exceeds the timeout.
    """
    sub_url = "educators/{0}/events"
    params = {"showNextTerm": int(next_term)}

    result = get(url=main_url + sub_url.format(educator_id),
                 params=params,
                 timeout=timeout)

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Get educator events", result)

    return result.json()


def search_educator(query, timeout=5):
    """
    Gets educators by searching their's last name or a part of last name.
    :param query: The last name search query.
    :type query: str
    :param timeout: (Optional) request timeout in seconds
    :type timeout: int
    :return: The result parsed to a JSON dictionary.
    :rtype: dict
    :raises spbu.ApiException: if `response status code` is not 200.
    :raises requests.exceptions.ReadTimeout: if the request exceeds the timeout.
    """
    sub_url = "educators/search/{0}"

    result = get(url=main_url + sub_url.format(query),
                 timeout=timeout)

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Search educator", result)

    return result.json()
