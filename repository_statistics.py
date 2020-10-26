#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
from typing import NamedTuple
from datetime import datetime


ACCEPT = "application/vnd.github.v3+json"
URL_BASE = "https://api.github.com"
PER_PAGE = 100


class Params(NamedTuple):
    """Параметры отчета"""
    url: str
    api_key: str
    begin_date: datetime
    end_date: datetime
    branch: str = "master"


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
    result_page: list
    header_link: str
    header_content_length: int


def get_date_from_str(date_str: str) -> datetime:
    """
    Конвертировать строку в дату.
    :param date_str:
    :return:
    """
    return datetime.strptime(date_str, "%d.%m.%Y")


def get_valid_params(func: object) -> Params:
    """
    Декоратор валидации параметров.
    Возвращает параметры или бросает исклюсение на некорректном параметре.
    :param func:
    :return:
    """
    pass


def is_url(url: str) -> bool:
    """
    Валидация параметра url
    :param url:
    :return:
    """
    pass


def is_branch(branch: str) -> bool:
    """
    Валидация наименования ветки
    :param branch:
    :return:
    """
    pass


@get_valid_params
def get_params(url: str, begin_date: str, end_date: str, branch: str) -> Params:
    """
    Формирует структуру для хранения параметров скрипта
    :param url:
    :param begin_date:
    :param end_date:
    :param branch:
    :return:
    """
    pass


def get_last_parts_url(url: str, num_parts: int) -> str:
    """
    Получает с конца из строки часть url ресурса в зависимости от параметра num_parts.
    :param url: url ресурса
    :param num_parts: количество частей в пространстве имен, которое будет извлечено
    :return:
    """
    return "/".join(url.split("/")[-num_parts:])


def get_url_parameters_for_commits_github(params: Params) -> dict:
    """
    Получить словарь параметров для формирования endpoint запроса по коммитам
    :param params:
    :return:
    """
    pass

def get_endpoint_url_for_commits_github(url: str, url_params: dict) -> str:
    """
    Формирует url для отправки запроса на получение данных по коммитам
    :param url:
    :param url_params:
    :return:
    """
    pass


def get_url_parameters_for_pull_requests_github(params: Params, is_open: bool, is_old: bool) -> dict:
    """
    Получить словарь параметров для формирования endpoint запроса по pull requests
    :param params:
    :param is_open:
    :param is_old:
    :return:
    """
    pass


def get_endpoint_url_for_pull_requests_github(url: str, url_params: dict) -> str:
    """
    Формирует url для отправки запроса на получение данных по pull requests
    :param url:
    :param url_params:
    :return:
    """
    pass

def get_url_parameters_for_issues_github(params: Params, is_open: bool, is_old: bool) -> dict:
    """
    Получить словарь параметров для формирования endpoint запроса по issues
    :param params:
    :param is_open:
    :param is_old:
    :return:
    """
    pass


def get_endpoint_url_for_pull_issues_github(url: str, url_params: dict) -> str:
    """
    Формирует url для отправки запроса на получение данных по issues
    :param url:
    :param url_params:
    :return:
    """
    pass


def get_headers(api_key: str) -> dict:
    """
    Формирует заголовок запроса
    :param api_key:
    :return:
    """
    return {'Accept': ACCEPT, 'Authorization': "Token {}".format(api_key)}


def get_num_of_pages(url: str, headers: dict) -> int:
    """
    Получает число страниц ответа для пагинации
    :param url:
    :param headers:
    :return:
    """
    pass


def get_response_data(full_url: str, headers: dict) -> ResponseData:
    """
    Получить ответ на запрос с заголовками
    :param full_url:
    :param headers:
    :return: именованный кортеж с именами полей result_page, header_link, header_content_length
    """
    pass


def get_dev_activity(params: Params) -> DevActivity:
    """
    Формирует запрос на получение данных и отправляет их на парсинг.
    Получает статистику разработчиков по количеству коммитов.
    :param params:
    :return:
    """
    pass


def parse_dev_activity_from_github_page(commit_list: list) -> DevActivity:
    """
    Парсинг данных о статистике коммитов со страницы GitHub.
    :param commit_list:
    :return:
    """
    pass


def get_pull_requests(params: Params) -> PullRequests:
    """
    Формирует запрос на получение данных и отправляет их на парсинг.
    Получает статистику pull requests.
    :param params:
    :return:
    """
    pass


def parse_pull_requests_from_github_page(pull_requests_list: list) -> PullRequests:
    """
    Парсинг данных о статистике pull requests со страницы GitHub.
    :param pull_requests_list:
    :return:
    """
    pass


def get_issues(params: Params) -> Issues:
    """
    Формирует запрос на получение данных и отправляет их на парсинг.
    Получает статистику issues.
    :param params:
    :return:
    """
    pass


def parse_issues_from_github_page(issues_list: list) -> Issues:
    """
    Парсинг данных о статистике issues со страницы GitHub.
    :param issues_list:
    :return:
    """
    pass


def get_result_data(params: Params) -> ResultData:
    """
    Получает результирующий набор данных.
    Запуск функций поиска осуществляется опционально.
    :param params:
    :return:
    """
    pass
    # dev_activity = get_dev_activity(params)
    # pull_requests = get_pull_requests(params)
    # issues = get_issues(params)


def output_data(result_data: ResultData):
    """
    Вывод результатов работы скрипта.
    :param result_data:
    :return:
    """
    pass


@click.command()
@click.argument('url')
@click.argument('begin_date')
@click.argument('end_date')
@click.argument('branch')
def main(url, begin_date, end_date, branch):
    params = get_params(url, begin_date, end_date, branch)
    result_data = get_result_data(params)
    output_data(result_data)


if __name__ == "__main__":
    main()
