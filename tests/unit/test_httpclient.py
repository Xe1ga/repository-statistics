import pytest

from unittest.mock import patch

from repository_statistics.httpclient import get_response_content_with_pagination
from repository_statistics.structure import ResponseData

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
