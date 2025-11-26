from decimal import Decimal
import pytest

from .calculator import calculator, correct_action, correct_value


@pytest.fixture
def run_calculator():
    def run(value1, value2, action, monkeypatch):
        data = iter([value1, value2, action])
        monkeypatch.setattr("builtins.input", lambda *args: next(data))
        value1 = correct_value("Введите первое число:")
        value2 = correct_value("Введите второе число:")
        action = correct_action("Введите операцию:")
        answer = calculator(value1, value2, action)
        return answer
    return run


@pytest.mark.parametrize(
    "value1, value2, action, result",
    (
        ("5", "2", "+", Decimal(7)),
        ("5", "2", "-", Decimal(3)),
        ("5", "2", "/", Decimal("2.5")),
        ("5", "2", "*", Decimal(10))
    )
)
def test_str(
    value1, value2, action, result, run_calculator, monkeypatch
):
    answer = run_calculator(value1, value2, action, monkeypatch)
    assert answer == result


@pytest.mark.parametrize(
    "value1, value2, action, result",
    (
        (5, 2, "+", Decimal(7)),
        (5, 2, "-", Decimal(3)),
        (5, 2, "/", Decimal("2.5")),
        (5, 2, "*", Decimal(10))
    )
)
def test_int(
    value1, value2, action, result, run_calculator, monkeypatch
):
    answer = run_calculator(value1, value2, action, monkeypatch)
    assert answer == result


@pytest.mark.parametrize(
    "value1, value2, action, result",
    (
        (5.5, 2.5, "+", Decimal(8)),
        (5.5, 2.5, "-", Decimal(3)),
        (5.5, 2.5, "/", Decimal("2.2")),
        (5.5, 2.5, "*", Decimal("13.75"))
    )
)
def test_float(
    value1, value2, action, result, run_calculator, monkeypatch
):
    answer = run_calculator(value1, value2, action, monkeypatch)
    assert answer == result


@pytest.mark.parametrize(
    "value1, value2, action",
    (
        ("worl", 2.5, "+"),
        (5.5, "home", "-")
    )
)
def test_wrong_value(
    value1, value2, action, run_calculator, monkeypatch, capsys
):
    with pytest.raises(StopIteration):
        run_calculator(value1, value2, action, monkeypatch)
    captured = capsys.readouterr()
    assert "Введите корректное число" in captured.out


def test_wrong_action(
   run_calculator, monkeypatch, capsys
):
    with pytest.raises(StopIteration):
        run_calculator("5", "2", "null", monkeypatch)
    captured = capsys.readouterr()
    assert "Введите корректную операцию" in captured.out
