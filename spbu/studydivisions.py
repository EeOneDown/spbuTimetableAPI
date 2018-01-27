# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from requests import get

from spbu.apiexception import ApiException
from spbu.consts import main_url


def get_study_divisions():
    """
    Gets study divisions.
    :return: The result parsed to a JSON dictionary.
    :rtype: list
    :raises ApiException: if `response status code` is not 200.
    """
    sub_url = "study/divisions"

    result = get(url=main_url + sub_url)

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Get extracur events", result)

    return result.json()


def get_program_levels(alias):
    """
    Gets study programs with levels for a given study division.
    :param alias: The division's short name code (alias).
    :type alias: str
    :return: The result parsed to a JSON dictionary.
    :rtype: list
    :raises ApiException: if `response status code` is not 200.
    """
    sub_url = "study/divisions/{0}/programs/levels"

    result = get(url=main_url + sub_url.format(alias))

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Get extracur events", result)

    return result.json()
