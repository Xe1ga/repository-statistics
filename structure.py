# -*- coding: utf-8 -*-

"""
repository_statistic.structure
~~~~~~~~~~~~~~~~~~~

Модуль содержит структуры данных, используемые в проекте
"""
from typing import NamedTuple, Optional
from datetime import datetime

class Params(NamedTuple):
    """Параметры отчета"""
    url: str
    api_key: str
    begin_date: Optional[datetime]
    end_date: Optional[datetime]
    branch: str
    dev_activity: bool
    pull_requests: bool
    issues: bool


class PullRequests(NamedTuple):
    """Статистика pull requests"""
    open_pull_requests: int
    closed_pull_requests: int
    old_pull_requests: int


class Issues(NamedTuple):
    """Статистика issues"""
    open_issues: int
    closed_issues: int
    old_issues: int


class ResultData(NamedTuple):
    """Результирующий набор данных"""
    dev_activity: Optional[list[tuple]]
    pull_requests: Optional[PullRequests]
    issues: Optional[Issues]


class ResponseData(NamedTuple):
    """Структура хранит десериализованный объект ответа и заголовки"""
    response_json: Optional[list]
    links: Optional[dict]
    rate_limit_remaining: Optional[int]
    rate_limit_reset: Optional[datetime]
    status_code: int


class HeadersData(NamedTuple):
    """заголовки ответа, необходимые для валидации входных параметров"""
    links: Optional[dict]
    rate_limit_remaining: Optional[int]
    rate_limit_reset: Optional[datetime]
    status_code: int