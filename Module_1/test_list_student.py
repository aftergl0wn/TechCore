import pytest

from .list_student import filter_list


@pytest.fixture
def value_list():
    return [
        {
            "name": "Вася",
            "avg_grade": 5,
        },
        {
            "name": "Петя",
            "avg_grade": 1.5,
        },
        {
            "name": "Тася",
            "avg_grade": 2.2,
        },
        {
            "name": "Нина",
            "avg_grade": 8,
        },
        {
            "name": "Маша",
            "avg_grade": 9,
        },
    ]


@pytest.fixture
def right_list():
    return [
        {
            "name": "Вася",
            "avg_grade": 5,
        },
        {
            "name": "Нина",
            "avg_grade": 8,
        },
        {
            "name": "Маша",
            "avg_grade": 9,
        },
    ]


def test_list_student(value_list, right_list):
    result = filter_list(value_list)
    assert result == right_list
    assert all(value["avg_grade"] > 4 for value in result)
