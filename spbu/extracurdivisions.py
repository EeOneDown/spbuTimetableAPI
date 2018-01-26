from datetime import date

from requests import get

from spbu.apiexception import ApiException
from spbu.consts import main_url


def get_extracur_divisions():
    """
    Gets extracurricular divisions.
    :raises: ApiException: if `response status code` is not 200.
    :return: The result parsed to a JSON dictionary.
    """
    sub_url = "extracur/divisions"

    result = get(url=main_url + sub_url)

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Get extracur divisions", result)

    return result.json()


def get_extracur_events(alias: str, from_date: date = None):
    """
    Get extracurricular events for a given division.
    :raises: ApiException: if `response status code` is not 200.
    :param: alias: The division's short name code (alias).
    :param: from_date: (Optional) The date the events start from.
    :return: The result parsed to a JSON dictionary.
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
