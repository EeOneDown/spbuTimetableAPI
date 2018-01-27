from requests import get

from spbu.apiexception import ApiException
from spbu.consts import main_url


def get_educator_events(educator_id: int, next_term=False):
    """
    Gets an educator's events for the current study term.
    :raises: ApiException: if `response status code` is not 200.
    :param: educator_id: The educator's id.
    :param: next_term: (Optional) Whether to show the events for the next term.
    :return: The result parsed to a JSON dictionary.
    """
    sub_url = "educators/{0}/events"
    params = {"showNextTerm": int(next_term)}

    result = get(url=main_url + sub_url.format(educator_id),
                 params=params)

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Get educator events", result)

    return result.json()


def search_educator(query: str):
    """
    Gets educators by searching their's last name or a part of last name.
    :raises: ApiException: if `response status code` is not 200.
    :param: query: The last name search query.
    :return: The result parsed to a JSON dictionary.
    """
    sub_url = "educators/search/{0}"

    result = get(url=main_url + sub_url.format(query))

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Search educator", result)

    return result.json()
