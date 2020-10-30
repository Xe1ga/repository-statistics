#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import requests

from typing import NamedTuple, Optional
from datetime import datetime
from json.decoder import JSONDecodeError

from exceptions import TimeoutError, ConnectionError, HTTPError, ValidationError


ACCEPT = "application/vnd.github.v3+json"
PER_PAGE = 100


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


def get_date_from_str(date_str: str) -> datetime:
    """
    Конвертировать строку в дату.
    :param date_str:
    :return:
    """
    return datetime.strptime(date_str, "%d.%m.%Y")


def get_base_api_url(url: str) -> str:
    """
    Получить коренной endpoint api необходимого ресурса
    :param url:
    :return:
    """
    if "github" in url:
        return "https://api.github.com"


def get_api_url_limit(url: str) -> str:
    """
    Получить коренной endpoint api необходимого ресурса
    :param url:
    :return:
    """
    return get_base_api_url(url) + "/rate_limit"


def get_api_url_branch(url: str) -> str:
    """
    Получить коренной endpoint api необходимого ресурса
    :param url:
    :return:
    """
    if "github" in url:
        return "https://api.github.com/rate_limit"


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
    return {'Accept': ACCEPT, 'Authorization': f'Token {api_key}'}


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


def is_api_key(url: str, api_key: str) -> bool:
    """
    Проверка корректности api_key
    :param url:
    :param api_key:
    :return:
    """
    try:
        return get_response_headers_data(
            get_api_url_limit(url),
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
        date = get_date_from_str(date)
    except ValueError:
        return False
    return True


def is_branch(branch: str) -> bool:
    """
    Валидация наименования ветки
    :param branch:
    :return:
    """
    try:
        return get_response_headers_data(
            get_api_url_limit(url),
            headers=get_headers(api_key)
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

    if not is_api_key(params["url"], params["api_key"]):
        errors.append('Авторизация не удалась. Вероятно, некорректный api_key.')

    if params["begin_date"] and not is_date(params["begin_date"]):
        errors.append(f'Неккорректно задан параметр даты начала периода, {params["begin_date"]}.')

    if params["end_date"] and not is_date(params["end_date"]):
        errors.append(f'Неккорректно задан параметр даты конца периода, {params["end_date"]}.')

    if not is_branch(params["branch"]):
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


def _get_response(url: str, method: str, parameters: Optional[dict] = None, headers: Optional[dict] = None) -> requests.Response:
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
        404: "Не прошла авторизация. Проверьте корректность api_key.",
        403: "Доступ к ресурсу ограничен.",
        404: "Запрашиваемый ресурс не найден. Проверьте корректность url."
    }

    try:
        response = getattr(requests, method)(url, params=parameters, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise TimeoutError("Превышен таймаут получения ответа от сервера.")
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Проблема соединения с сервером.")
    except requests.exceptions.HTTPError:
        if http_error_codes.get(response.status_code):
            raise HTTPError(http_error_codes.get(response.status_code))
        else:
            raise HTTPError(f"Возникла HTTP ошибка, код ошибки: {response.status_code}.")
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
    except ValidationError as err:
        print("Проверьте правильность указания параметров скрипта:\n", "\n".join(err.message))
    except (TimeoutError, ConnectionError) as err:
        print("Проверьте подключение к сети:\n", err)

    # result_data = get_result_data(params)
    # output_data(result_data)


if __name__ == "__main__":
    main()
