from decimal import Decimal, InvalidOperation


def correct_value(name):
    while True:
        try:
            value = Decimal(input(name))
            return value
        except InvalidOperation:
            print("Введите корректное число")


def correct_action(name):
    while True:
        action = input(name)
        if action in '+-/*':
            return action
        else:
            print("Введите корректную операцию")


def calculator(value1, value2, action):
    if action == "+":
        return (value1+value2)
    elif action == "-":
        return (value1-value2)
    elif action == "/":
        return (value1/value2)
    elif action == "*":
        return (value1*value2)


if __name__ == "__main__":
    value1 = correct_value("Введите первое число:")
    value2 = correct_value("Введите второе число:")
    action = correct_action("Введите операцию:")
    result = calculator(value1, value2, action)
    print(f"Результат: {result}")
