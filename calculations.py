#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional

from sites.github import (endpoints, get_url_parameters_for_commits, get_url_parameters_for_pull_requests,
                          get_url_parameters_for_issues, parse_dev_activity_from_page, parse_obj_search_from_page)
from structure import Params, PullRequests, Issues, ResultData
from httpclient import get_response_content_with_pagination

def get_commits_page_content(params: Params) -> list:
    """
    Получает список словарей, содержащий информацию о коммитах
    :param params:
    :return:
    """
    url = endpoints["commits"](params.url)
    parameters = get_url_parameters_for_commits(params)
    return get_response_content_with_pagination(params, url, parameters)


def get_pull_requests_page_content(params: Params, is_open: bool) -> list:
    """
    Формирует запрос на получение данных и отправляет их на парсинг.
    Получает статистику pull requests.
    :param params:
    :param is_open:
    :return:
    """
    url = endpoints["pulls"](params.url)
    parameters = get_url_parameters_for_pull_requests(params, is_open)
    return get_response_content_with_pagination(params, url, parameters)


def get_issues_page_content(params: Params, is_open: bool) -> list:
    """
    Формирует запрос на получение данных и отправляет их на парсинг.
    :param params:
    :param is_open:
    :return:
    """
    url = endpoints["issues"](params.url)
    parameters = get_url_parameters_for_issues(is_open)
    return get_response_content_with_pagination(params, url, parameters)


def get_dev_activity(params: Params) -> Optional[list]:
    """
    Получить количество коммитов (опционально)
    :param params:
    :return:
    """
    return parse_dev_activity_from_page(get_commits_page_content(params)) if params.dev_activity else None


def get_pull_requests(params: Params) -> Optional[PullRequests]:
    """
    Получить статистику pull request (опционально)
    :param params:
    :return:
    """
    return PullRequests(
        parse_obj_search_from_page(
            params,
            get_pull_requests_page_content(params, is_open=True),
        ),
        parse_obj_search_from_page(
            params,
            get_pull_requests_page_content(params, is_open=False),
        ),
        parse_obj_search_from_page(
            params,
            get_pull_requests_page_content(params, is_open=True),
            is_old=True
        )
    ) if params.pull_requests else None


def get_issues(params: Params) -> Optional[Issues]:
    """
    Получить статистику pull request (опционально)
    :param params:
    :return:
    """
    return Issues(
        parse_obj_search_from_page(
            params,
            get_issues_page_content(params, is_open=True),
        ),
        parse_obj_search_from_page(
            params,
            get_issues_page_content(params, is_open=False),
        ),
        parse_obj_search_from_page(
            params,
            get_issues_page_content(params, is_open=True),
            is_old=True
        )
    ) if params.issues else None


def get_result_data(params: Params) -> ResultData:
    """
    Получает результирующий набор данных.
    Запуск функций поиска осуществляется опционально.
    :param params:
    :return:
    """
    return ResultData(
        get_dev_activity(params),
        get_pull_requests(params),
        get_issues(params)
    )
