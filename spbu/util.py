import os
from typing import Union

from requests import get, Response

from spbu.consts import APIMethods, BASE_URL
from spbu.types import ApiException


default_timeout = int(os.getenv('SPBU_TT_API_REQUEST_TIMEOUT', '5'))


def _make_request(url: str, params: dict = None,
                  timeout: int = default_timeout) -> Response:
    return get(url, params, timeout=timeout)


def call_api(method: APIMethods, path_values: dict = None,
             params: dict = None) -> Union[dict, list]:
    res = _make_request(
        BASE_URL + method.value.format(**(path_values or {})), params
    )
    if res.status_code != 200:
        msg = f'The server returned HTTP {res.status_code} {res.reason}. ' \
            f'Response body:\n[{res.text}]'
        raise ApiException(msg, method.name, res)

    return res.json()
