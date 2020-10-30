# -*- coding: utf-8 -*-

"""
repository_statistic.utils
~~~~~~~~~~~~~~~~~~~

Модуль общие функции, которые могут использоваться в нескольких модулях проекта
"""
from datetime import datetime


def get_date_from_str(date_str: str) -> datetime:
    """
    Конвертировать строку в дату.
    :param date_str:
    :return:
    """
    return datetime.strptime(date_str, "%d.%m.%Y")


def get_last_parts_url(url: str, num_parts: int) -> str:
    """
    Получает с конца из строки часть url ресурса в зависимости от параметра num_parts.
    :param url: url ресурса
    :param num_parts: количество частей в пространстве имен, которое будет извлечено
    :return:
    """
    return "/".join(url.split("/")[-num_parts:])