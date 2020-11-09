#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import requests

from datetime import datetime
from typing import Optional
from json.decoder import JSONDecodeError

from sites.github import (endpoints, get_headers, get_url_parameters_for_commits, get_url_parameters_for_pull_requests,
                          get_url_parameters_for_issues, parse_dev_activity_from_page, parse_obj_search_from_page)
from exceptions import TimeoutConnectionError, ConnectError, HTTPError, ValidationError
from utils import get_date_from_str, get_begin_date, get_end_date
from structure import Params, PullRequests, Issues, ResultData, ResponseData, HeadersData


def is_url(url: str) -> bool:
    """
    Валидация параметра url
    :param url:
    :return:
    """
    try:
        return get_response_headers_data(url).status_code == 200
    except HTTPError:
        return False


def is_api_key(api_key: str) -> bool:
    """
    Проверка корректности api_key
    :param api_key:
    :return:
    """
    try:
        return get_response_headers_data(
            endpoints['limit'],
            headers=get_headers(api_key)
        ).status_code == 200
    except HTTPError:
        return False


def is_date(date: str) -> bool:
    """
    Валидация даты
    :param date:
    :return:
    """
    try:
        get_date_from_str(date)
    except ValueError:
        return False
    return True


def is_branch(url: str, branch: str) -> bool:
    """
    Валидация наименования ветки
    :param url:
    :param branch:
    :return:
    """
    try:
        return get_response_headers_data(
            endpoints["branch"](url, branch)
        ).status_code == 200
    except HTTPError:
        return False


def get_validation_errors(**params) -> list:
    """
    Формирует общее сообщение об ошибках валидации параметров.
    :param params:
    :return:
    """
    errors = []

    if not is_url(params["url"]):
        errors.append(f'Неккорректно задан параметр url или репозитория с адресом {params["url"]} не существует.')

    if not is_api_key(params["api_key"]):
        errors.append('Авторизация не удалась. Вероятно, некорректный api_key.')

    if params["begin_date"] and not is_date(params["begin_date"]):
        errors.append(f'Неккорректно задан параметр даты начала периода, {params["begin_date"]}.')

    if params["end_date"] and not is_date(params["end_date"]):
        errors.append(f'Неккорректно задан параметр даты конца периода, {params["end_date"]}.')

    if not is_branch(params["url"], params["branch"]):
        errors.append(f'Ветки репозитория с указанным именем {params["branch"]} не существует.')

    return errors


def get_valid_params(func: object) -> Params:
    """
    Декоратор валидации параметров.
    Возвращает параметры или бросает исключение и выводит общее сообщение об ошибках валидации.
    :param func:
    :return:
    """
    def wrapper(**params):
        validation_errors = get_validation_errors(**params)
        if validation_errors:
            raise ValidationError(validation_errors)
        else:
            params = func(**params)
            return params

    return wrapper


@get_valid_params
def get_params(**params) -> Params:
    """
    Формирует структуру для хранения параметров скрипта
    :param params:
    :return:
    """
    return Params(
        url=params["url"],
        api_key=params["api_key"],
        begin_date=get_begin_date(params["begin_date"]) if params["begin_date"] else None,
        end_date=get_end_date(params["end_date"]) if params["end_date"] else None,
        branch=params["branch"],
        dev_activity=params["dev_activity"],
        pull_requests=params["pull_requests"],
        issues=params["issues"]
    )


def get_next_pages(links: dict) -> str:
    """
    Возвращает адрес следующей страницы
    :param links:
    :return:
    """
    return links.get("next").get("url") if links.get("next") else ""


def _get_response(
        url: str,
        method: str,
        parameters: Optional[dict] = None,
        headers: Optional[dict] = None
) -> requests.Response:
    """
    Получить объект ответа requests.Response
    :param method:
    :param url:
    :param parameters:
    :param headers:
    :return:
    """
    if parameters is None:
        parameters = {}

    if headers is None:
        headers = {}

    http_error_codes = {
        401: "Не прошла авторизация. Проверьте корректность api_key.",
        403: "Доступ к ресурсу ограничен.",
        404: "Запрашиваемый ресурс не найден. Проверьте корректность url."
    }

    try:
        response = getattr(requests, method)(url, params=parameters, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise TimeoutConnectionError("Превышен таймаут получения ответа от сервера.")
    except requests.exceptions.ConnectionError:
        raise ConnectError("Проблема соединения с сервером.")
    except requests.exceptions.HTTPError as err:
        raise HTTPError(
            http_error_codes.get(
                err.response.status_code,
                f"Возникла HTTP ошибка, код ошибки: {err.response.status_code}."
            )
        )
    return response


def get_response_headers_data(
        url: str, parameters: Optional[dict] = None,
        headers: Optional[dict] = None
) -> HeadersData:
    """
    Получает заголовки ответа
    :param url:
    :param parameters:
    :param headers:
    :return:
    """
    response = _get_response(url, method="head", parameters=parameters, headers=headers)

    return HeadersData(
        response.links,
        response.headers.get('X-RateLimit-Remaining'),
        datetime.fromtimestamp(
            int(response.headers.get('X-RateLimit-Reset'))
        ) if response.headers.get('X-RateLimit-Reset') else None,
        response.status_code,
    )


def get_response_data(url: str, parameters: Optional[dict] = None, headers: Optional[dict] = None) -> ResponseData:
    """
    Получить десериализованные данные ответа Response и часть необходимых заголовков
    :param url:
    :param parameters:
    :param headers:
    :return:
    """
    response = _get_response(url, method="get", parameters=parameters, headers=headers)

    try:
        response_json = response.json()
    except (ValueError, JSONDecodeError):
        response_json = None

    return ResponseData(
        response_json,
        response.links,
        response.headers.get('X-RateLimit-Remaining'),
        datetime.fromtimestamp(
            int(response.headers.get('X-RateLimit-Reset'))
        ) if response.headers.get('X-RateLimit-Reset') else None,
        response.status_code,
    )


def get_response_content_with_pagination(params: Params, url: str, parameters: dict) -> list:
    """
    Формирует список словарей - объектов поиска постранично и возвращает его
    :param params:
    :param url:
    :param parameters:
    :return:
    """
    content = []
    while url:
        data = get_response_data(
            url,
            parameters,
            get_headers(params.api_key)
            )
        content.extend(data.response_json)
        url = get_next_pages(data.links)
        parameters = None
    return content


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


def output_data(result_data: ResultData):
    """
    Вывод результатов работы скрипта.
    :param result_data:
    :return:
    """
    print(f"COMMIT STATISTIC = {result_data.dev_activity}")
    print(f"Number of open pull requests = {result_data.pull_requests.open_pull_requests}")
    print(f"Number of closed pull requests = {result_data.pull_requests.closed_pull_requests}")
    print(f"Number of old pull requests = {result_data.pull_requests.old_pull_requests}")
    print(f"Number of open issues = {result_data.issues.open_issues}")
    print(f"Number of closed issues = {result_data.issues.closed_issues}")
    print(f"Number of old pull issues = {result_data.issues.old_issues}")


@click.command()
@click.argument('url', type=str)
@click.argument('api_key', type=str)
@click.option(
    '--begin_date', '-b', type=str, default="",
    help='analysis start date in format "dd.mm.YYYY"'
)
@click.option(
    '--end_date', '-e', type=str, default="",
    help='analysis end date in format "dd.mm.YYYY"'
)
@click.option(
    '--branch', '-br', type=str, default="master",
    help='repository branch name'
)
@click.option(
    '--dev_activity', '-da', is_flag=True,
    help='analyze developer activity'
)
@click.option(
    '--pull_requests', '-pr', is_flag=True,
    help='analysis of the pull requests on a given branch of the repository'
)
@click.option(
    '--issues', '-i', is_flag=True,
    help='analysis of issues on a given branch of the repository'
)
def main(url, api_key, begin_date, end_date, branch, dev_activity, pull_requests, issues):
    """
    Script for analyzing repository statistics according to the specified parameters.
    If the start and end dates of the analysis are not specified,
    then an unlimited interval is taken to the left, right or completely.
    If the repository branch is not specified, the master branch is taken by default.
    The following events are optionally analyzed:

        1. The activity of developers by the number of commits (--dev_activity).

        2. Statistics of merge requests (--pull_requests).

        3. Issues statistics (--issues).

    If none of the options is specified, then the analysis will be carried out in all directions.
    """
    try:
        params = get_params(
                url=url,
                api_key=api_key,
                begin_date=begin_date,
                end_date=end_date,
                branch=branch,
                dev_activity=dev_activity if True in (dev_activity, pull_requests, issues) else True,
                pull_requests=pull_requests if True in (dev_activity, pull_requests, issues) else True,
                issues=issues if True in (dev_activity, pull_requests, issues) else True
            )
    except ValidationError as err:
        print("Проверьте правильность указания параметров скрипта:\n", "\n".join(err.message))
    except (TimeoutConnectionError, ConnectError) as err:
        print("Проверьте подключение к сети:\n", err)
    else:
        output_data(get_result_data(params))


if __name__ == "__main__":
    main()