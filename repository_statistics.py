#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
from typing import NamedTuple
from datetime import datetime


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
    api_key: str
    cmd_input: bool


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
    :return:
    """
    pass


if __name__ == "__main__":
    conf = get_conf()
    params = get_params(conf.cmd_input)
