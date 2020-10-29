# -*- coding: utf-8 -*-

"""
repository_statistic.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set exceptions.
"""
class Error(Exception):
    """
    Базовое исключение проекта
    """
    def __init__(self, message):
        self.message = message


class TimeoutError(Error):
    """
    Исключение, возникающее при превышении таймаута установки соединения с сервером
    или превышении таймаут ожидания ответа от сервера
    """


class ConnectionError(Error):
    """
    Исключение, возникающее при проблемах соединения с сервером
    """


class NotFoundError(Error):
    """
    Исключение, возникающее при HTTP ошибке 404, когда запрашиваемый ресурс не найден
    """