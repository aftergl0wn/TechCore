from decimal import Decimal, InvalidOperation


def correct_value(name):
    while True:
        value = input(name)
        try:
            value_dec = Decimal(value)
            return value_dec
        except InvalidOperation:
            return value


def correct_action(name):
    while True:
        action = input(name)
        if action in '+-/*':
            return action
        else:
            print("Введите корректную операцию")


def calculator(value1, value2, action):
    all_str = isinstance(value1, str) and isinstance(value2, str)
    all_dec = isinstance(value1, Decimal) and isinstance(value2, Decimal)
    if not all_str and not all_dec:
        if isinstance(value1, Decimal):
            value1 = int(value1)
        else:
            value2 = int(value2)
    if action == "+" and (all_str or all_dec):
        return (value1+value2)
    elif action == "-" and all_dec:
        return (value1-value2)
    elif action == "/" and all_dec:
        return (value1/value2)
    elif action == "*":
        return (value1*value2)
    else:
        return "Невозможно совершить данную операцию"


if __name__ == "__main__":
    value1 = correct_value("Введите первое число:")
    value2 = correct_value("Введите второе число:")
    action = correct_action("Введите операцию:")
    result = calculator(value1, value2, action)
    print(f"Результат: {result}")
