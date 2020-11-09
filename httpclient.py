#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

from typing import Optional
from datetime import datetime
from json.decoder import JSONDecodeError

from structure import Params, ResponseData, HeadersData
from exceptions import TimeoutConnectionError, ConnectError, HTTPError


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


def get_response_content_with_pagination(url: str, parameters: dict, headers: dict):
    """
    Формирует список словарей - объектов поиска постранично и возвращает его
    :param url:
    :param parameters:
    :param headers:
    :return:
    """
    while url:
        data = get_response_data(
            url,
            parameters,
            headers
            )
        yield data.response_json
        url = get_next_pages(data.links)
        parameters = None
