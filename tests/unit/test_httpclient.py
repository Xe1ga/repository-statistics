import pytest

from unittest.mock import patch, Mock

from repository_statistics.httpclient import get_response_content_with_pagination, _get_response, requests
from repository_statistics.structure import ResponseData
from repository_statistics.exceptions import TimeoutConnectionError, ConnectError, HTTPError


request_attributes = [
    ('https://good/url',
     {'sha': 'master', 'since': '2020-10-01T00:00:00', 'until': '2020-10-31T23:59:59.999999', 'per_page': '100'},
     {'Accept': 'application/vnd.github.v3+json', 'Authorization': 'Token'},
     {"created_at": "date", "author": {"login": "max-ott"}}
     )
]

request_attributes_with_method = [
    ('https://good/url',
     'get',
     {'Accept': 'application/vnd.github.v3+json', 'Authorization': 'Token'},
     {'sha': 'master', 'since': '2020-10-01T00:00:00', 'until': '2020-10-31T23:59:59.999999', 'per_page': '100'}
     ),
    ('https://good/url',
     'head',
     {'Accept': 'application/vnd.github.v3+json', 'Authorization': 'Token'},
     {'sha': 'master', 'since': '2020-10-01T00:00:00', 'until': '2020-10-31T23:59:59.999999', 'per_page': '100'}
     )

]


def get_structure_response_data(*args, **kwargs):
    response_json = [{
        "created_at": "date",
        "author": {"login": "max-ott"},
    }]
    links = dict(next={"url": "good"})
    return ResponseData(
        response_json=response_json,
        links=links,
        rate_limit_remaining=None,
        rate_limit_reset=None,
        status_code=200
    )


@pytest.mark.parametrize('url, parameters, headers, result', request_attributes)
def test_get_response_content_with_pagination(url, parameters, headers, result):
    with patch('repository_statistics.httpclient.get_response_data') as mock_get_response_data:
        with patch('repository_statistics.httpclient.get_next_pages') as mock_get_next_pages:
            mock_get_response_data.side_effect = get_structure_response_data
            mock_get_next_pages.return_value = ""
            parameters = (url, parameters, headers)
            data = get_response_content_with_pagination(parameters)
            assert next(data) == result
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
@patch.object(requests, 'head', return_value=Mock(status_code=200,
                                                  json={"created_at": "date", "author": {"login": "max-ott"}}))
@patch.object(requests, 'get', return_value=Mock(status_code=200,
                                                 json={"created_at": "date", "author": {"login": "max-ott"}}))
def test_get_response(mock_requests_get, mock_requests_head, url, method, parameters, headers):
    response = _get_response(url, method, parameters, headers)
    assert response.json == {"created_at": "date", "author": {"login": "max-ott"}}
