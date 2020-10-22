#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
from collections import namedtuple
from typing import NamedTuple
from datetime import datetime


ACCEPT = "application/vnd.github.v3+json"
URL_BASE = "https://api.github.com"


class Params(NamedTuple):
    """Параметры отчета"""
    url: str
    begin_date: datetime
    end_date: datetime
    branch: str


class Config(NamedTuple):
    """Параметры конфигурационного файла"""
    api_key: str
    cmd_input: bool


class DevActivity(NamedTuple):
    """Статистика разработчиков по количеству коммитов"""
    login: str
    number_of_commits: int


class PullRequests(NamedTuple):
    """Статистика разработчиков по количеству коммитов"""
    open_pull_requests: int
    closed_pull_requests: int
    old_pull_requests: int

    def __str__(self):
        return "Number of open pull requests = {}.\n" \
               "Number of closed pull requests = {}.\n" \
               "Number of old pull requests = {}.\n".format(
                   str(self.open_pull_requests),
                   str(self.closed_pull_requests),
                   str(self.old_pull_requests)
               )


def get_conf() -> Config:
    """Получает данные из файла конфигурации"""
    try:
        config = configparser.RawConfigParser()
        config.read("config.ini")
        api_key = config.get("Parameters", "API_KEY")
        cmd_input = config.get("Parameters", "CMD_INPUT")
        result = Config(api_key, cmd_input)
        return result

    except Exception:
        print("Problem loading data from config.ini file.")
        return None


def get_params(cmd_input: bool = True) -> Params:
    """
    Получает параметры из источника в зависимости от cmd_input
    :param cmd_input:
    :return: типизированный именованный кортеж с параметрами отчета
    """
    pass


def get_limit_data(api_key: str) -> LimitData:
    """
    Получить статус ограничения скорости для аутентифицированного пользователя
    :param api_key:
    :return: именованный кортеж с именами полей limit, remaining, reset
    """
    LimitData = namedtuple("LimitData", "limit remaining reset")
    full_url = URL_BASE + "/rate_limit"
    headers = {'Accept': ACCEPT, 'Authorization': "Token {}".format(api_key)}
    # получаем количество страниц ответа
    response_data = get_response_data(full_url, headers)
    print("Core limit = " + str(response_data.result_page.get("resources").get("core").get("limit"))
          + "(remaining = " + str(response_data.result_page.get("resources").get("core").get("remaining"))
          + ")." + "\n"
          + "Reset: "
          + str(datetime.fromtimestamp(response_data.result_page.get("resources").get("core").get("reset"))))
    if response_data.result_page:
        result = LimitData(response_data.result_page.get("resources").get("core").get("limit"),
                           response_data.result_page.get("resources").get("core").get("remaining"),
                           response_data.result_page.get("resources").get("core").get("reset"))
    else:
        result = None
    return result


def get_response_data(full_url: str, headers: dict) -> ResponseData:
    """
    Получить ответ на запрос с заголовками
    :param full_url:
    :param headers:
    :return: именованный кортеж с именами полей result_page, header_link, header_content_length
    """
    # LimitData = namedtuple("LimitData", "result_page header_link header_content_length")
    pass


if __name__ == "__main__":
    conf = get_conf()
    params = get_params(conf.cmd_input)
