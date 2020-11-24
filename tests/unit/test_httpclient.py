import pytest

from jsonschema import validate
from unittest.mock import patch, Mock

from repository_statistics.httpclient import (get_response_content_with_pagination,
                                              _get_response, requests, get_response_data)
from repository_statistics.structure import ResponseData
from repository_statistics.exceptions import TimeoutConnectionError, ConnectError, HTTPError


request_url = "http://url"
request_parameters = {'sha': 'master', 'since': '2020-10-01T00:00:00', 'until': '2020-10-31T23:59:59.999999', 'per_page': '100'}
request_headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': 'Token'}
result_json = {"created_at": "date", "author": {"login": "name"}}


request_attributes = [(request_url, request_parameters, request_headers)]


request_attributes_with_method = [(request_url, "get", request_parameters, request_headers),
                                  (request_url, "head", request_parameters, request_headers)]


mock_status_200 = Mock(status_code=200, json={"created_at": "date", "author": {"login": "name"}})


valid_schema = {"title": "response",
                "description": "response json",
                "type": "object",
                "properties": {"created_at": {"type": "string"},
                               "author": {"login": {"type": "string"}}},
                "required": ["created_at"]
}


def response_return_value(mock_function):
    mock_function.return_value.status_code = 200
    mock_function.return_value.json.return_value = result_json
    mock_function.return_value.links = {}
    mock_function.return_value.headers = {}


def get_structure_response_data(*args, **kwargs):
    response_json = [result_json]
    links = dict(next={"url": "good"})
    return ResponseData(
        response_json=response_json,
        links=links,
        rate_limit_remaining=None,
        rate_limit_reset=None,
        status_code=200
    )


@pytest.mark.parametrize('url, parameters, headers', request_attributes)
def test_get_response_content_with_pagination(url, parameters, headers):
    with patch('repository_statistics.httpclient.get_response_data') as mock_get_response_data:
        with patch('repository_statistics.httpclient.get_next_pages') as mock_get_next_pages:
            mock_get_response_data.side_effect = get_structure_response_data
            mock_get_next_pages.return_value = ""
            params = (url, parameters, headers)
            data = get_response_content_with_pagination(params)
            assert next(data) == result_json
            with pytest.raises(StopIteration):
                next(data)


@pytest.mark.parametrize('url, method, parameters, headers', request_attributes_with_method)
@patch.object(requests, 'head', side_effect=[requests.exceptions.Timeout(), requests.exceptions.ConnectionError()])
@patch.object(requests, 'get', side_effect=[requests.exceptions.Timeout(), requests.exceptions.ConnectionError()])
def test_get_response_err(mock_requests_get, mock_requests_head, url, method, parameters, headers):
    with pytest.raises(TimeoutConnectionError):
        _get_response(url, method, parameters, headers)
    with pytest.raises(ConnectError):
        _get_response(url, method, parameters, headers)


@pytest.mark.parametrize('url, method, parameters, headers', request_attributes_with_method)
@patch.object(requests, 'head', return_value=Mock(status_code=404))
@patch.object(requests, 'get', return_value=Mock(status_code=404))
def test_get_response_http_err(mock_requests_get, mock_requests_head, url, method, parameters, headers):
    # mock_requests_get.response.status_code = 404
    # mock_requests_head.response.status_code = 404
    mock_requests_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError
    mock_requests_head.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError
    mock_requests_get.return_value.raise_for_status.side_effect.response.status_code = 404
    mock_requests_head.return_value.raise_for_status.side_effect.response.status_code = 404
    with pytest.raises(HTTPError):
        _get_response(url, method, parameters, headers)


@pytest.mark.parametrize('url, method, parameters, headers', request_attributes_with_method)
@patch.object(requests, 'head')
@patch.object(requests, 'get')
def test_get_response_200_ok(mock_requests_get, mock_requests_head, url, method, parameters, headers):
    response_return_value(mock_requests_get if method == "get" else mock_requests_head)
    response = _get_response(url, method, parameters, headers)
    assert response.json() == result_json


@pytest.mark.parametrize('url, parameters, headers', request_attributes)
@patch('repository_statistics.httpclient._get_response')
def test_get_response_data_200_ok(mock_get_response, url, parameters, headers):
    response_return_value(mock_get_response)
    response_data = get_response_data(url, parameters, headers)
    validate(response_data.response_json, valid_schema)
    assert response_data.response_json == result_json
