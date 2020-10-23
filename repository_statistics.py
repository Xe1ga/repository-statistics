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
    branch: str


class DevActivity(NamedTuple):
    """Статистика разработчиков по количеству коммитов"""
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
    dev_activity: DevActivity
    pull_requests: PullRequests
    issues: Issues


class ResponseData(NamedTuple):
    """Структура хранит десериализованный объект ответа и заголовки"""
    result_page: list
    header_link: str
    header_content_length: int


# @click.command()
# @click.argument('url')
def get_params() -> Params:
    """
    Получает входные параметры
    :return: типизированный именованный кортеж с параметрами отчета
    """
    pass


def is_valid_params(params: Params) -> bool:
    """
    Валидация параметров
    :param params:
    :return:
    """


def is_url(url: str) -> bool:
    """
    Валидация параметра url
    :param url:
    :return:
    """
    pass


def is_date(begin_date: str) -> bool:
    """
    Валидация параметра даты
    :param begin_date:
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


def get_part_url(url: str) -> str:
    """
    Получает часть url по типу {логин}/{имя репозитория} из полного url
    :param url:
    :return:
    """
    return "/".join(url.split("/")[-2:])


def get_url(part_url: str, git_obj: str) -> str:
    """
    Получает первую часть url (без параметров) для запроса по коммитам
    :param part_url:
    :param git_obj: "commits" или "pulls" или "issues"
    :return:
    """
    if git_obj == "commits":
        return URL_BASE + "/repos/" + part_url + "/commits"
    elif git_obj == "pulls":
        return URL_BASE + "/repos/" + part_url + "/pulls"
    elif git_obj == "issues":
        return URL_BASE + "/repos/" + part_url + "/issues"


def get_url_parameters(params: Params, git_obj: str, state: bool, old: bool) -> dict:
    """
    Формирует словарь параметров url
    :param params:
    :param git_obj: "commits" или "pulls" или "issues"
    :param state: статус True - открыто, False - закрыто
    :param old: True - "старый" pull request или issue, False - "свежий"
    :return:
    """
    pass


def get_url_with_params(params: Params, git_obj: str, state: bool, old: bool) -> str:
    """
    Получение полного url с параметрами
    :param params:
    :param git_obj:
    :param state:
    :param old:
    :return: строка, содержит полный url запроса
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


if __name__ == "__main__":
    params = get_params()
    result_data = None
    if is_valid_params(params):
        result_data = get_result_data(params)
        output_data(result_data)
