# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from requests import models

from spbu.consts import error_msg


class ApiException(Exception):
    """
    This class represents an Exception thrown when a call to the SPbU TimeTable
    API fails.
    In addition to an informative message, it has a `function_name` and a
    `result` attribute, which respectively contain the name of the failed
    function and the returned result that made the function to be considered
    as failed.
    """
    def __init__(self, msg, function_name, result):
        """
        :param msg: error message
        :type msg: str
        :param function_name: The name of function which raise the exception
        :type function_name: str
        :param result: request response
        :type result: models.Response
        """
        super(ApiException, self).__init__(error_msg.format(msg))
        self.function_name = function_name
        self.result = result
