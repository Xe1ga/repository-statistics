import pytest
from datetime import datetime

import repository_statistics.validation


@pytest.mark.parametrize('date_to_check', [
    pytest.param('29.02.2019', id='february 29'),
    pytest.param('01.13.2020', id='invalid range'),
    pytest.param('2020.02.10', id='reverse order'),
    pytest.param('05/10/1985', id='invalid separator'),
    pytest.param('ррррр55555', id='arbitrary string'),
    pytest.param(10051978, id='not string'),
    pytest.param(datetime.now(), id='object')])
def test_is_date_false(date_to_check):
    """Функция is_date() должна сгенерироваь исключение на неверно указанный параметр даты"""
    assert repository_statistics.validation.is_date(date_to_check) is False


@pytest.mark.parametrize('date_to_check', [
    pytest.param('01.05.1999', id='good date behind'),
    pytest.param('22.12.2055', id='good date ahead')])
def test_is_date_true(date_to_check):
    """Функция is_date() должна сгенерироваь исключение на неверно указанный параметр даты"""
    assert repository_statistics.validation.is_date(date_to_check) is True
