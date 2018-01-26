from requests import get

from spbu.apiexception import ApiException
from spbu.consts import main_url


def get_study_divisions():
    """
    Gets study divisions.
    :raises: ApiException: if `response status code` is not 200.
    :return: The result parsed to a JSON dictionary.
    """
    sub_url = "study/divisions"

    result = get(url=main_url + sub_url)

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Get extracur events", result)

    return result.json()


def get_program_levels(alias: str):
    """
    Gets study programs with levels for a given study division.
    :raises: ApiException: if `response status code` is not 200.
    :param: alias: The division's short name code (alias).
    :return: The result parsed to a JSON dictionary.
    """
    sub_url = "study/divisions/{0}/programs/levels"

    result = get(url=main_url + sub_url.format(alias))

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Get extracur events", result)

    return result.json()
