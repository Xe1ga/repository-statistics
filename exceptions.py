# -*- coding: utf-8 -*-

"""
repository_statistic.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set exceptions.
"""
class TimeoutError(Exception):
    """
    Исключение, возникающее при превышении таймаута установки соединения с сервером
    или превышении таймаут ожидания ответа от сервера
    """
    def __init__(self, message):
        self.message = message


class ConnectionError(Exception):
    """
    Исключение, возникающее при проблемах соединения с сервером
    """
    def __init__(self, message):
        self.message = message


class NotFoundError(Exception):
    """
    Исключение, возникающее при HTTP ошибке 404, когда запрашиваемый ресурс не найден
    """
    def __init__(self, message):
        self.message = message


