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
