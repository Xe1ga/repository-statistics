#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional
from functools import reduce

from sites.github import (parse_dev_activity_from_page, select_issues,
                          select_pull_requests)
from structure import Params, PullRequests, Issues, ResultData
from exceptions import TimeoutConnectionError, ConnectError, HTTPError, ParseError


def get_dev_activity(params: Params) -> Optional[list]:
    """
    Получить количество коммитов (опционально)
    :param params:
    :return:
    """
    return parse_dev_activity_from_page(params) if params.dev_activity else None


def get_pull_requests(params: Params) -> Optional[PullRequests]:
    """
    Получить статистику pull request (опционально)
    :param params:
    :return:
    """
    return PullRequests(
        reduce(
            lambda x, y: x + y,
            select_pull_requests(params, is_open=True)
            ),
        reduce(
            lambda x, y: x + y,
            select_pull_requests(params, is_open=False)
        ),
        reduce(
            lambda x, y: x + y,
            select_pull_requests(params, is_open=True, is_old=True)
        )
    ) if params.pull_requests else None


def get_issues(params: Params) -> Optional[Issues]:
    """
    Получить статистику pull request (опционально)
    :param params:
    :return:
    """
    return Issues(
        reduce(
            lambda x, y: x + y,
            select_issues(params, is_open=True)
        ),
        reduce(
            lambda x, y: x + y,
            select_issues(params, is_open=False)
        ),
        reduce(
            lambda x, y: x + y,
            select_issues(params, is_open=True, is_old=True)
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


def run(params: Params) -> ResultData:
    """
    Запуск вычислений
    :param params:
    :return:
    """
    try:
        result_data = get_result_data(params)
    except (TimeoutConnectionError, ConnectError) as err:
        print("Проверьте подключение к сети:\n", err)
    except (HTTPError, ParseError) as err:
        print(err.message)
    else:
        return result_data
