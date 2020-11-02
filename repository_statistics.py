#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import click
import requests

from typing import Optional
from datetime import datetime
from json.decoder import JSONDecodeError

import errors
import sites

from utils import get_date_from_str, get_last_parts_url
from structure import Params, DevActivity, PullRequests, Issues, ResultData, ResponseData, HeadersData


def get_header_to_request(url: str, api_key: str) -> dict:
    """
    Получить заголовки для HTTP запроса к требуемому ресурсу
    :param url:
    :param api_key:
    :return:
    """
    if "github" in url:
        return sites.github.get_headers(api_key)


def get_base_api_url(url: str) -> str:
    """
    Получить коренной endpoint api необходимого ресурса
    :param url:
    :return:
    """
    if "github" in url:
        return "https://api.github.com"


def get_api_url_repos_part(url: str) -> str:
    """
    Получить часть url, endpoint репозитория, для github это /repos/ для bitbucket /repositories/
    :param url:
    :return:
    """
    if "github" in url:
        return "/repos/"


def get_api_url_branch_part(url: str) -> str:
    """
    Получить часть url, endpoint для веток
    :param url:
    :return:
    """
    if "github" in url:
        return "/branches/"


def get_api_url_commits_part(url: str) -> str:
    """
    Получить часть url, endpoint для коммитов
    :param url:
    :return:
    """
    if "github" in url:
        return "/commits"


def get_api_url_pull_requests_part(url: str) -> str:
    """
    Получить часть url, endpoint для pull requests
    :param url:
    :return:
    """
    if "github" in url:
        return "/pulls"


def get_api_url_branch(url: str, branch: str) -> str:
    """
    Получить  endpoint api поиска ветки репозитория
    :param url:
    :param branch:
    :return:
    """
    return f"{get_base_api_url(url)}" \
           f"{get_api_url_repos_part(url)}" \
           f"{get_last_parts_url(url, 2)}" \
           f"{get_api_url_branch_part(url)}" \
           f"{branch}"


def get_endpoint_url_for_commits(url: str) -> str:
    """
    Формирует url для отправки запроса на получение данных по коммитам
    :param url:
    :return:
    """
    return f"{get_base_api_url(url)}" \
           f"{get_api_url_repos_part(url)}" \
           f"{get_last_parts_url(url, 2)}" \
           f"{get_api_url_branch_part(url)}" \
           f"{get_api_url_commits_part(url)}"


def get_endpoint_url_for_pull_requests(url: str) -> str:
    """
    Формирует url для отправки запроса на получение данных по pull requests
    :param url:
    :return:
    """
    return f"{get_base_api_url(url)}" \
           f"{get_api_url_repos_part(url)}" \
           f"{get_last_parts_url(url, 2)}" \
           f"{get_api_url_pull_requests_part(url)}"


def get_endpoint_url_for_pull_issues_github(url: str) -> str:
    """
    Формирует url для отправки запроса на получение данных по issues
    :param url:
    :return:
    """
    pass


def is_url(url: str) -> bool:
    """
    Валидация параметра url
    :param url:
    :return:
    """
    try:
        return get_response_headers_data(url).status_code == 200
    except errors.exceptions.HTTPError:
        return False


def is_api_key(url: str, api_key: str) -> bool:
    """
    Проверка корректности api_key
    :param url:
    :param api_key:
    :return:
    """
    try:
        return get_response_headers_data(
            sites.github.get_api_url_limit(url),
            headers=get_header_to_request(url, api_key)
        ).status_code == 200
    except errors.exceptions.HTTPError:
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
            get_api_url_branch(url, branch)
        ).status_code == 200
    except errors.exceptions.HTTPError:
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

    if not is_api_key(params["url"], params["api_key"]):
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
            raise errors.exceptions.ValidationError(validation_errors)
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
        begin_date=get_date_from_str(params["begin_date"]) if params["begin_date"] else None,
        end_date=get_date_from_str(params["end_date"]) if params["end_date"] else None,
        branch=params["branch"],
        dev_activity=params["dev_activity"],
        pull_requests=params["pull_requests"],
        issues=params["issues"]
    )


def get_num_of_pages(url: str, headers: dict) -> int:
    """
    Получает число страниц ответа для пагинации
    :param url:
    :param headers:
    :return:
    """
    pass


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
        raise errors.exceptions.TimeoutError("Превышен таймаут получения ответа от сервера.")
    except requests.exceptions.ConnectionError:
        raise errors.exceptions.ConnectionError("Проблема соединения с сервером.")
    except requests.exceptions.HTTPError:
        raise errors.exceptions.HTTPError(
            http_error_codes.get(
                response.status_code,
                f"Возникла HTTP ошибка, код ошибки: {response.status_code}."
            )
        )
    return response


def get_response_headers_data(url: str, parameters: Optional[dict] = None, headers: Optional[dict] = None) -> HeadersData:
    """
    Получает заголовки ответа
    :param url:
    :param parameters:
    :param headers:
    :return:
    """
    response = _get_response(url, method="head", parameters=parameters, headers=headers)

    return HeadersData(
        response.headers.get('Link'),
        response.headers.get('Content-Length'),
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
        response.headers.get('Link'),
        response.headers.get('Content-Length'),
        response.headers.get('X-RateLimit-Remaining'),
        datetime.fromtimestamp(
            response.headers.get('X-RateLimit-Reset')
        ) if response.headers.get('X-RateLimit-Reset') else None,
        response.status_code,
    )


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


def parse_pull_requests_from_github_page(pull_requests_list: list, is_old: bool) -> PullRequests:
    """
    Парсинг данных о статистике pull requests со страницы GitHub.
    :param pull_requests_list:
    :param is_old:
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


def parse_issues_from_github_page(issues_list: list, is_old: bool) -> Issues:
    """
    Парсинг данных о статистике issues со страницы GitHub.
    :param issues_list:
    :param is_old:
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
                dev_activity=dev_activity,
                pull_requests=pull_requests,
                issues=issues
            )
    except errors.exceptions.ValidationError as err:
        print("Проверьте правильность указания параметров скрипта:\n", "\n".join(err.message))
    except (errors.exceptions.TimeoutError, errors.exceptions.ConnectionError) as err:
        print("Проверьте подключение к сети:\n", err)
    print(os.path)


if __name__ == "__main__":
    main()
