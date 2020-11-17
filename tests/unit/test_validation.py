import pytest
import repository_statistics.validation


def test_is_date():
    """Функция is_date() должна сгенерироваь исключение на неверно указанный параметр даты"""
    is_date = repository_statistics.validation.is_date('01.13.2020')
    assert is_date is False
