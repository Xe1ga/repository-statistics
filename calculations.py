#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional

from sites.github import count_commits_by_author, count_issues, count_pulls
from structure import Params, PullRequests, Issues, ResultData


def get_dev_activity(params: Params) -> Optional[list]:
    """
    Получить количество коммитов (опционально)
    :param params:
    :return:
    """
    return count_commits_by_author(params) if params.dev_activity else None


def get_pull_requests(params: Params) -> Optional[PullRequests]:
    """
    Получить статистику pull request (опционально)
    :param params:
    :return:
    """
    return PullRequests(
        count_pulls(params, is_open=True),
        count_pulls(params, is_open=False),
        count_pulls(params, is_open=True, is_old=True)
    ) if params.pull_requests else None


def get_issues(params: Params) -> Optional[Issues]:
    """
    Получить статистику pull request (опционально)
    :param params:
    :return:
    """
    return Issues(
        count_issues(params, is_open=True),
        count_issues(params, is_open=False),
        count_issues(params, is_open=True, is_old=True)
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
