# -*- coding: utf-8 -*-

"""
repository_statistic.github
~~~~~~~~~~~~~~~~~~~

Модуль содержит специфичные для github функции
"""
from utils import add_one_to_val
from repository_statistics import get_base_api_url
from structure import Params, DevActivity, PullRequests, Issues


ACCEPT = "application/vnd.github.v3+json"
PER_PAGE = 100


def get_headers(api_key: str) -> dict:
    """
    Формирует заголовок запроса
    :param api_key:
    :return:
    """
    return {'Accept': ACCEPT, 'Authorization': f'Token {api_key}'}


def get_api_url_limit(url: str) -> str:
    """
    Получить endpoint api ограничения скорости
    :param url:
    :return:
    """
    return f"{get_base_api_url(url)}/rate_limit"


def get_url_parameters_for_commits(params: Params) -> dict:
    """
    Получить словарь параметров для формирования endpoint запроса по коммитам
    :param params:
    :return:
    """
    url_parameters = {
        'sha': params.branch,
        'since': params.begin_date,
        'until': params.end_date,
        'per_page': str(PER_PAGE)
    }

    return {key: value for key, value in url_parameters.items() if value is not None}


def get_url_parameters_for_pull_requests(params: Params, is_open: bool) -> dict:
    """
    Получить словарь параметров для формирования endpoint запроса по pull requests
    :param params:
    :param is_open:
    :return:
    """
    url_parameters = {
        'state': "open" if is_open else "closed",
        'base': params.branch,
        'per_page': str(PER_PAGE)
    }

    return url_parameters


def get_url_parameters_for_issues(is_open: bool) -> dict:
    """
    Получить словарь параметров для формирования endpoint запроса по issues
    :param is_open:
    :return:
    """
    url_parameters = {
        'state': "open" if is_open else "closed",
        'per_page': str(PER_PAGE)
    }

    return url_parameters


def parse_dev_activity_from_page(commits: list) -> list:
    """
    Подсчет данных о статистике коммитов в разрезе разработчиков на GitHub.
    :param commits:
    :return:
    """
    pass

