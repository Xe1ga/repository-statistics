# -*- coding: utf-8 -*-

"""
repository_statistic.github
~~~~~~~~~~~~~~~~~~~

Модуль содержит специфичные для github функции
"""
from collections import Counter
from datetime import datetime


from exceptions import ParseError
from structure import Params
from utils import get_date_from_str_without_time, in_interval, get_last_parts_url
from httpclient import get_response_content_with_pagination


ACCEPT = "application/vnd.github.v3+json"
PER_PAGE = 100
NUM_DAYS_OLD_PULL_REQUESTS = 30
NUM_DAYS_OLD_ISSUES = 14
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


def get_endpoint_parameters_for_commits(params: Params) -> tuple:
    """
    Получает список словарей, содержащий информацию о коммитах
    :param params:
    :return:
    """
    url = endpoints["commits"](params.url)
    parameters = get_url_parameters_for_commits(params)
    headers = get_headers(params.api_key)
    return url, parameters, headers


def get_endpoint_parameters_for_pull_requests(params: Params, is_open: bool) -> tuple:
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


def get_endpoint_parameters_for_issues(params: Params, is_open: bool) -> tuple:
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
    url, parameters, headers = get_endpoint_parameters_for_commits(params)
    for page in get_response_content_with_pagination(url, parameters, headers):
        for commit in page:
            if commit.get("author"):
                result.append(commit.get("author").get("login"))

    return Counter(result).most_common(30)


def parse_obj_search_from_page(params: Params, obj_search: str, is_open: bool, is_old: bool = False) -> int:
    """
    Парсинг данных о статистике pull requests и issues со страницы GitHub.
    :param params:
    :param obj_search:
    :param is_open:
    :param is_old:
    :return:
    """
    result = 0
    url, parameters, headers = get_endpoint_parameters(params, obj_search, is_open)
    for page in get_response_content_with_pagination(url, parameters, headers):
        for obj_search in page:
            if obj_search.get("created_at"):
                if in_interval(
                        get_date_from_str_without_time(params.begin_date),
                        get_date_from_str_without_time(params.end_date),
                        get_date_from_str_without_time(obj_search.get("created_at"))
                ) and clarify_by_issue(obj_search) and (True if not is_old else is_old_obj_search(obj_search)):
                    result += 1

    return result


def get_endpoint_parameters(params: Params, obj_search: str, is_open: bool) -> tuple:
    """
    Возвращает endpoint и headers для pulls и issues
    :param params:
    :param obj_search:
    :param is_open:
    :return:
    """
    if "pulls" in obj_search:
        return get_endpoint_parameters_for_pull_requests(params, is_open)
    else:
        return get_endpoint_parameters_for_issues(params, is_open)


def is_old_obj_search(obj_search: dict) -> bool:
    """
    Возвращает True или False в зависисмости от того, является ли pull request или issue старым
    :param obj_search:
    :return:
    """
    url = obj_search.get("url")
    if "pulls" in url:
        num_days = NUM_DAYS_OLD_PULL_REQUESTS
    elif "issues" in url:
        num_days = NUM_DAYS_OLD_ISSUES
    else:
        raise ParseError("Ошибка парсинга страницы.")
    date_diff = abs(datetime.now().date() - get_date_from_str_without_time(obj_search.get("created_at"))).days

    return date_diff > num_days


def clarify_by_issue(obj_search: dict) -> bool:
    """
    Уточнить является issue не связанной с pull requests
    :param obj_search:
    :return:
    """
    return not ("issue" in obj_search.get("url") and obj_search.get("pull_request"))
