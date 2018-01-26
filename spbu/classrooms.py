from datetime import datetime

from requests import get

from spbu.apiexception import ApiException
from spbu.consts import main_url


def create_string_from_datetime(dt: datetime):
    """
    Creates a specific string from a datetime object.
    :param dt: A datetime object.
    :return: Specific sting.
    """
    return dt.strftime("%Y%m%d%H%M")


def is_classroom_busy(oid: str, start: datetime, end: datetime):
    """
    Checks whether a given classroom is busy in a specified interval
    or it's part.
    :raises: ApiException: if `response status code` is not 200.
    :param: oid: The classroom's id.
    :param: start: The interval's start.
    :param: end: The interval's end.
    :return: The result parsed to a JSON dictionary.
    """
    sub_url = "classrooms/{0}/isbusy/{1}/{2}"
    start = create_string_from_datetime(start)
    end = create_string_from_datetime(end)

    result = get(url=main_url + sub_url.format(oid, start, end))

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Is classroom busy", result)

    return result.json()
