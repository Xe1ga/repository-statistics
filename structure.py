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


class DevActivity(NamedTuple):
    """Статистика одного разработчика по количеству коммитов"""
    login: str
    number_of_commits: int


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
    dev_activity: list[DevActivity]
    pull_requests: PullRequests
    issues: Issues


class ResponseData(NamedTuple):
    """Структура хранит десериализованный объект ответа и заголовки"""
    response_json: Optional[list]
    link: Optional[str]
    content_length: Optional[int]
    rate_limit_remaining: Optional[int]
    rate_limit_reset: Optional[datetime]
    status_code: int


class HeadersData(NamedTuple):
    """заголовки ответа, необходимые для валидации входных параметров"""
    link: Optional[str]
    content_length: Optional[int]
    rate_limit_remaining: Optional[int]
    rate_limit_reset: Optional[datetime]
    status_code: int