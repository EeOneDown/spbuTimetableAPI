from requests import get

from spbu.apiexception import ApiException
from spbu.consts import main_url


def get_groups(program_id: int):
    """
    Gets a given study program's student groups for the current study year.
    :raises: ApiException: if `response status code` is not 200.
    :param: program_id: The study program's id.
    :return: The result parsed to a JSON dictionary.
    """
    sub_url = "progams/{0}/groups"

    result = get(url=main_url + sub_url.format(program_id))

    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, "Get extracur events", result)

    return result.json()
