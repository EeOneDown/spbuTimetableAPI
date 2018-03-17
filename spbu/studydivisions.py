# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from requests import get

from spbu.consts import main_url
from spbu.types import ApiException


def get_study_divisions(timeout=5):
    """
    Gets study divisions.
    :param timeout: (Optional) request timeout in seconds
    :type timeout: int
    :return: The result parsed to a JSON dictionary.
    :rtype: list
    :raises spbu.ApiException: if `response status code` is not 200.
    :raises requests.exceptions.ReadTimeout: if the request exceeds the timeout.
    """
    sub_url = "study/divisions"

    result = get(url=main_url + sub_url,
                 timeout=timeout)

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Get extracur events", result)

    return result.json()


def get_program_levels(alias, timeout=5):
    """
    Gets study programs with levels for a given study division.
    :param alias: The division's short name code (alias).
    :type alias: str
    :param timeout: (Optional) request timeout in seconds
    :type timeout: int
    :return: The result parsed to a JSON dictionary.
    :rtype: list
    :raises spbu.ApiException: if `response status code` is not 200.
    :raises requests.exceptions.ReadTimeout: if the request exceeds the timeout.
    """
    sub_url = "study/divisions/{0}/programs/levels"

    result = get(url=main_url + sub_url.format(alias),
                 timeout=timeout)

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Get extracur events", result)

    return result.json()
