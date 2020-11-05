# -*- coding: utf-8 -*-

"""
repository_statistic.github
~~~~~~~~~~~~~~~~~~~

Модуль содержит специфичные для github функции
"""
from collections import Counter
from datetime import datetime

from repository_statistics import get_base_api_url
from structure import Params
from utils import get_date_from_str_without_time, in_interval


ACCEPT = "application/vnd.github.v3+json"
PER_PAGE = 100
NUM_DAYS_OLD_PULL_REQUESTS = 30
NUM_DAYS_OLD_ISSUES = 14


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
    Парсинг данных о статистике коммитов в разрезе разработчиков на GitHub.
    :param commits:
    :return:
    """
    result = []

    for commit in commits:
        if commit.get("author"):
            result.append(commit.get("author").get("login"))

    return Counter(result).most_common(30)


def parse_pull_requests_from_page(params: Params, pull_requests_list: list) -> int:
    """
    Парсинг данных о статистике pull requests со страницы GitHub.
    :param params:
    :param pull_requests_list:
    :return:
    """
    result = 0

    for pull_request in pull_requests_list:
        if pull_request.get("created_at"):
            if in_interval(
                    get_date_from_str_without_time(params.begin_date),
                    get_date_from_str_without_time(params.end_date),
                    get_date_from_str_without_time(pull_request.get("created_at"))
            ):
                result += 1
    return result


def parse_pull_requests_old_from_page(params: Params, pull_requests_list: list) -> int:
    """
    Парсинг данных о статистике old pull requests со страницы GitHub.
    :param params:
    :param pull_requests_list:
    :return:
    """
    result = 0

    for pull_request in pull_requests_list:
        if pull_request.get("created_at"):
            if in_interval(
                    get_date_from_str_without_time(params.begin_date),
                    get_date_from_str_without_time(params.end_date),
                    get_date_from_str_without_time(pull_request.get("created_at"))
            ) and is_old_obj_search(pull_request, NUM_DAYS_OLD_PULL_REQUESTS):
                result += 1
    return result


def is_old_obj_search(obj_search: dict, num_days: int) -> bool:
    """
    Возвращает True или False в зависисмости от того, является ли pull request или issue старым
    :param obj_search:
    :param num_days:
    :return:
    """
    return (abs(datetime.now().date() - get_date_from_str_without_time(obj_search.get("created_at"))).days
            > num_days)


def parse_issues_from_page(params: Params, issues_list: list) -> int:
    """
    Парсинг данных о статистике issues со страницы GitHub.
    :param params:
    :param issues_list:
    :return:
    """
    result = 0

    for issue in issues_list:
        if issue.get("created_at"):
            if in_interval(
                    get_date_from_str_without_time(params.begin_date),
                    get_date_from_str_without_time(params.end_date),
                    get_date_from_str_without_time(issue.get("created_at"))
            ):
                result += 1
    return result


def parse_issues_old_from_page(params: Params, issues_list: list) -> int:
    """
    Парсинг данных о статистике old issues со страницы GitHub.
    :param params:
    :param issues_list:
    :return:
    """
    result = 0

    for issue in issues_list:
        if issue.get("created_at"):
            if in_interval(
                    get_date_from_str_without_time(params.begin_date),
                    get_date_from_str_without_time(params.end_date),
                    get_date_from_str_without_time(issue.get("created_at"))
            ) and is_old_obj_search(issue, NUM_DAYS_OLD_ISSUES):
                result += 1
    return result
