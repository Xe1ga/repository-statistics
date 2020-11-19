import pytest

from unittest.mock import patch

from repository_statistics import validation


parameters = [
    (None, None),
    (None, '19.11.2020'),
    ('01.11.2020', None),
    ('01.11.2020', '19.11.2020')
]


@pytest.mark.parametrize('date_to_check', [
    pytest.param('29.02.2019', id='february 29'),
    pytest.param('01.13.2020', id='invalid range'),
    pytest.param('2020.02.10', id='reverse order'),
    pytest.param('05/10/1985', id='invalid separator'),
    pytest.param('ррррр55555', id='arbitrary string')])
def test_is_date_false(date_to_check):
    """Функция is_date() должна вернуть false на неверно указанный параметр даты"""
    assert not validation.is_date(date_to_check)


@pytest.mark.parametrize('date_to_check', [
    pytest.param('01.05.1999', id='good date behind'),
    pytest.param('22.12.2055', id='good date ahead')])
def test_is_date_true(date_to_check):
    """Функция is_date() должна вернуть True на корректно указанный параметр даты"""
    assert validation.is_date(date_to_check)


@patch('repository_statistics.validation.is_url')
@patch('repository_statistics.validation.is_api_key')
@patch('repository_statistics.validation.is_date')
@patch('repository_statistics.validation.is_branch')
@pytest.mark.parametrize('begin_date, end_date', parameters)
def test_date_in_get_validation_errors(is_url, is_api_key, is_date, is_branch, begin_date, end_date):
    """Тестируем валидацию параметров begin_date и end_date"""
    is_url.configure_mock(return_value=True)
    is_api_key.configure_mock(return_value=True)
    is_date.configure_mock(return_value=True)
    is_branch.configure_mock(return_value=True)
    errors = validation.get_validation_errors(
        url=None,
        api_key=None,
        begin_date=begin_date,
        end_date=end_date,
        branch=None
    )
    assert not errors
