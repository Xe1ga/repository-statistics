#!/usr/bin/env python
# -*- coding: utf-8 -*-
from repository_statistics.sites.github import endpoints, get_headers
from repository_statistics.exceptions import HTTPError, ValidationError
from repository_statistics.utils import get_date_from_str
from repository_statistics.structure import Params
from repository_statistics.httpclient import get_response_headers_data


def is_url(url: str) -> bool:
    """
    Валидация параметра url
    :param url:
    :return:
    """
    try:
        return get_response_headers_data(url).status_code == 200
    except HTTPError:
        return False


def is_api_key(api_key: str) -> bool:
    """
    Проверка корректности api_key
    :param api_key:
    :return:
    """
    try:
        return get_response_headers_data(
            endpoints['limit'],
            headers=get_headers(api_key)
        ).status_code == 200
    except HTTPError:
        return False


def is_date(date: str) -> bool:
    """
    Валидация даты
    :param date:
    :return:
    """
    try:
        get_date_from_str(date)
    except ValueError:
        return False
    return True


def is_branch(url: str, branch: str) -> bool:
    """
    Валидация наименования ветки
    :param url:
    :param branch:
    :return:
    """
    try:
        return get_response_headers_data(
            endpoints["branch"](url, branch)
        ).status_code == 200
    except HTTPError:
        return False


def get_validation_errors(**params) -> list:
    """
    Формирует общее сообщение об ошибках валидации параметров.
    :param params:
    :return:
    """
    errors = []

    if not is_url(params["url"]):
        errors.append(f'Неккорректно задан параметр url или репозитория с адресом {params["url"]} не существует.')

    if not is_api_key(params["api_key"]):
        errors.append('Авторизация не удалась. Вероятно, некорректный api_key.')

    if params["begin_date"] and not is_date(params["begin_date"]):
        errors.append(f'Неккорректно задан параметр даты начала периода, {params["begin_date"]}.')

    if params["end_date"] and not is_date(params["end_date"]):
        errors.append(f'Неккорректно задан параметр даты конца периода, {params["end_date"]}.')

    if (params["begin_date"] and params["end_date"] and is_date(params["begin_date"]) and is_date(params["end_date"])
            and get_date_from_str(params["begin_date"]) > get_date_from_str(params["end_date"])):
        errors.append('Дата начала периода больше даты конца периода')

    if not is_branch(params["url"], params["branch"]):
        errors.append(f'Ветки репозитория с указанным именем {params["branch"]} не существует.')

    return errors


def get_valid_params(func: object) -> Params:
    """
    Декоратор валидации параметров.
    Возвращает параметры или бросает исключение и выводит общее сообщение об ошибках валидации.
    :param func:
    :return:
    """
    def wrapper(**params):
        validation_errors = get_validation_errors(**params)
        if validation_errors:
            raise ValidationError(validation_errors)
        else:
            params = func(**params)
            return params

    return wrapper
