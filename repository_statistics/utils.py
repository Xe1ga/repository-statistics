# -*- coding: utf-8 -*-

"""
repository_statistic.utils
~~~~~~~~~~~~~~~~~~~

Модуль общие функции, которые могут использоваться в нескольких модулях проекта
"""
from datetime import datetime, date
from typing import Optional


def get_begin_date(target_date: str) -> str:
    """
    Возвращает начальную дату с минимальным временем
    :param target_date:
    :return:
    """
    return get_min_time_in_date(get_date_from_str(target_date))


def get_end_date(target_date: str) -> str:
    """
    Возвращает начальную дату с максимальным временем
    :param target_date:
    :return:
    """
    return get_max_time_in_date(get_date_from_str(target_date))


def get_min_time_in_date(target_date: datetime) -> str:
    """
    Возвращает дату с минимальным временем
    :param target_date:
    :return:
    """
    return target_date.combine(target_date.date(), target_date.min.time()).isoformat()


def get_max_time_in_date(target_date: datetime) -> str:
    """
    Возвращает дату с максимальным временем
    :param target_date:
    :return:
    """
    return target_date.combine(target_date.date(), target_date.max.time()).isoformat()


def get_date_from_str(date_str: str) -> datetime:
    """
    Конвертировать строку в дату.
    :param date_str:
    :return:
    """
    return datetime.strptime(date_str, "%d.%m.%Y")


def get_date_from_str_without_time(date_str: str) -> date:
    """
    Возвращает дату в формате "%Y-%m-%d"
    :param date_str:
    :return:
    """
    return datetime.strptime(date_str[:10], "%Y-%m-%d").date() if date_str else None


def in_interval(begin_date: Optional[date], end_date: Optional[date], target_date: date) -> bool:
    """
    Проверка на вхождение даты date в интервал дат [begin_date; end_date]
    :param begin_date:
    :param end_date:
    :param target_date:
    :return:
    """
    return not ((target_date < begin_date if begin_date else False) or (target_date > end_date if end_date else False))


def get_last_parts_url(url: str, num_parts: int) -> str:
    """
    Получает с конца из строки часть url ресурса в зависимости от параметра num_parts.
    :param url: url ресурса
    :param num_parts: количество частей в пространстве имен, которое будет извлечено
    :return:
    """
    return "/".join(url.split("/")[-num_parts:])


def to_compare_with_current_date(num_days: int, created_date: str) -> bool:
    """
    Возвращает True, если количество дней от текущей даты превосходит заданное количество дней, иначе False
    :param created_date:
    :param num_days:
    :return:
    """
    return abs(datetime.now().date() - get_date_from_str_without_time(created_date)).days > num_days
