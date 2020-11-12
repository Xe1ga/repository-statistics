# -*- coding: utf-8 -*-

"""
repository_statistic.github
~~~~~~~~~~~~~~~~~~~

Модуль содержит специфичные для github функции
"""
from collections import Counter
from datetime import datetime
from functools import partial

from structure import Params
from utils import get_date_from_str_without_time, in_interval, get_last_parts_url
from httpclient import get_response_content_with_pagination

ACCEPT = "application/vnd.github.v3+json"
PER_PAGE = 100
NUM_DAYS_OLD_PULL_REQUESTS = 30
NUM_DAYS_OLD_ISSUES = 14
NUM_RECORDS = 30
BASE_URL = "https://api.github.com"

endpoints = {
    "limit": f"{BASE_URL}/rate_limit",
    "branch": lambda url, branch: f"{BASE_URL}/repos/{get_last_parts_url(url, 2)}/branches/{branch}",
    "commits": lambda url: f"{BASE_URL}/repos/{get_last_parts_url(url, 2)}/commits",
    "pulls": lambda url: f"{BASE_URL}/repos/{get_last_parts_url(url, 2)}/pulls",
    "issues": lambda url: f"{BASE_URL}/repos/{get_last_parts_url(url, 2)}/issues"

}


def get_headers(api_key: str) -> dict:
    """
    Формирует заголовок запроса
    :param api_key:
    :return:
    """
    return {'Accept': ACCEPT, 'Authorization': f'Token {api_key}'}


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


def get_request_attributes_for_commits(params: Params) -> tuple:
    """
    Получает список словарей, содержащий информацию о коммитах
    :param params:
    :return:
    """
    url = endpoints["commits"](params.url)
    parameters = get_url_parameters_for_commits(params)
    headers = get_headers(params.api_key)
    return url, parameters, headers


def get_request_attributes_for_pulls(params: Params, is_open: bool) -> tuple:
    """
    Формирует запрос на получение данных и отправляет их на парсинг.
    Получает статистику pull requests.
    :param params:
    :param is_open:
    :return:
    """
    url = endpoints["pulls"](params.url)
    parameters = get_url_parameters_for_pull_requests(params, is_open)
    headers = get_headers(params.api_key)
    return url, parameters, headers


def get_request_attributes_for_issues(params: Params, is_open: bool) -> tuple:
    """
    Формирует запрос на получение данных и отправляет их на парсинг.
    :param params:
    :param is_open:
    :return:
    """
    url = endpoints["issues"](params.url)
    parameters = get_url_parameters_for_issues(is_open)
    headers = get_headers(params.api_key)
    return url, parameters, headers


def parse_dev_activity_from_page(params: Params) -> list:
    """
    Парсинг данных о статистике коммитов в разрезе разработчиков на GitHub.
    :param params:
    :return:
    """
    result = []
    for commit in get_response_content_with_pagination(get_request_attributes_for_commits(params)):
        if commit.get("author"):
            result.append(commit.get("author").get("login"))
    return Counter(result).most_common(NUM_RECORDS)


def get_map_units_for_each_pulls(params: Params, is_open: bool, is_old: bool = False) -> map:
    """
    Получает объект map - итератор из единиц для каждого pull request, удовлетворяющего условиям отбора
    :param params:
    :param is_open:
    :param is_old:
    :return:
    """
    p_in_interval = partial(
        in_interval,
        get_date_from_str_without_time(params.begin_date),
        get_date_from_str_without_time(params.end_date)
    )
    is_old_pulls = partial(
        is_old_obj_search,
        NUM_DAYS_OLD_PULL_REQUESTS
    )

    return (map(lambda pr: 1,
                filter(
                    lambda pr: (p_in_interval(get_date_from_str_without_time(pr.get("created_at")))
                                and (is_old_pulls(pr.get("created_at")) if is_old else True)),
                    get_response_content_with_pagination(get_request_attributes_for_pulls(params, is_open))
                )
                )
            )


def get_map_units_for_each_issues(params: Params, is_open: bool, is_old: bool = False) -> map:
    """
    Отбирает из всех pull requests, удовлетворяющие параметрам скрипта
    :param params:
    :param is_open:
    :param is_old:
    :return:
    """
    p_in_interval = partial(
        in_interval,
        get_date_from_str_without_time(params.begin_date),
        get_date_from_str_without_time(params.end_date)
    )
    is_old_issue = partial(
        is_old_obj_search,
        NUM_DAYS_OLD_ISSUES
    )
    return (map(lambda issue: 1,
                filter(
                    lambda issue: (is_item_an_issue(issue)
                                   and p_in_interval(get_date_from_str_without_time(issue.get("created_at")))
                                   and (is_old_issue(issue.get("created_at")) if is_old else True)),
                    get_response_content_with_pagination(get_request_attributes_for_issues(params, is_open))
                )
                )
            )


def is_old_obj_search(created_date: str, num_days: int) -> bool:
    """
    Возвращает True или False в зависисмости от того, является ли pull request или issue старым
    :param created_date: 
    :param num_days: 
    :return: 
    """
    return abs(datetime.now().date() - get_date_from_str_without_time(created_date)).days > num_days


def is_item_an_issue(obj_search: dict) -> bool:
    """
    Уточнить является issue не связанной с pull requests
    :param obj_search:
    :return:
    """
    return not ("issue" in obj_search.get("url") and obj_search.get("pull_request"))
