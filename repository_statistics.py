#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
from collections import namedtuple
from typing import NamedTuple
from datetime import datetime


ACCEPT = "application/vnd.github.v3+json"
URL_BASE = "https://api.github.com"
PER_PAGE = 100


class Params(NamedTuple):
    """Параметры отчета"""
    url: str
    begin_date: datetime
    end_date: datetime
    branch: str


class Config(NamedTuple):
    """Параметры конфигурационного файла"""
    api_key: str


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


class ResponseData(NamedTuple):
    """Структура хранит десериализованный объект ответа и нужные для скрипта данные заголовка ответа"""
    result_page: list
    header_link: str
    header_content_length: int


def get_params() -> Params:
    """
    Получает входные параметры
    :return: типизированный именованный кортеж с параметрами отчета
    """
    pass


def input(url) -> Params:
    """
    Получает входные параметры
    :return: типизированный именованный кортеж с параметрами отчета
    """
    pass


def validation_url(url: str) -> bool:
    """
    Валилация параметра url
    :param url:
    :return:
    """


def validation_begin_date(begin_date: str) -> bool:
    """
    Валилация параметра даты начала отчета
    :param begin_date:
    :return:
    """


def validation_end_date(end_date: str) -> bool:
    """
    Валилация параметра даты конца отчета
    :param end_date:
    :return:
    """


def validation_branch(branch: str) -> bool:
    """
    Валидация наименования ветки
    :param branch:
    :return:
    """


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


def get_conf() -> Config:
    """Получает данные из файла конфигурации"""
    try:
        config = configparser.RawConfigParser()
        config.read("config.ini")
        api_key = config.get("Parameters", "API_KEY")
        result = Config(api_key)
        return result

    except Exception:
        print("Problem loading data from config.ini file.")
        return None


def get_response_data(full_url: str, headers: dict) -> ResponseData:
    """
    Получить ответ на запрос с заголовками
    :param full_url:
    :param headers:
    :return: именованный кортеж с именами полей result_page, header_link, header_content_length
    """
    pass


if __name__ == "__main__":
    conf = get_conf()
    params = get_params()
