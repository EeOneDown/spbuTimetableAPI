from datetime import date, timedelta

from requests import get

from spbu.apiexception import ApiException
from spbu.consts import main_url, available_lessons_types


def get_group_events(group_id: int, lessons_type="Unknown",
                     from_date: date = None, to_date: date = None):
    """
    Gets a given student group's events for the current week or
    Gets a given student group's events for a week starting from a specified
        datetime until the end of the week or
    Gets events for a specified date range.
    :raises: ApiException: if `response status code` is not 200.
    :param: group_id: The student group's id.
    :param: lessons_type: (Optional) The type of lessons type.
    :param: from_date: (Optional) The datetime the events start from.
    :param: to_date: (Optional) The datetime the events ends.
    :return: The result parsed to a JSON dictionary.
    """
    sub_url = "groups/{0}/events/{1}/{2}"
    params = {}

    if lessons_type in available_lessons_types:
        params["timetable"] = lessons_type

    if from_date is None:
        from_date = date.today()
        to_date = from_date + timedelta(days=7)
    elif to_date is None:
        to_date = from_date + timedelta(days=7)

    result = get(url=main_url + sub_url.format(group_id, from_date, to_date),
                 params=params)

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Get extracur events", result)

    return result.json()
