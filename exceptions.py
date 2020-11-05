# -*- coding: utf-8 -*-

"""
repository_statistic.exceptions
~~~~~~~~~~~~~~~~~~~

Модуль содержит собственные исключения проекта
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
    pass


class ConnectionError(Error):
    """
    Исключение, возникающее при проблемах соединения с сервером
    """
    pass


class HTTPError(Error):
    """
    Исключение, возникающее при HTTP ошибках
    """
    pass


class ValidationError(Error):
    """
    Исключение, возникающее при ошибках валидации
    """
    pass
