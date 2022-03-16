"""
1.Задание
Ввести произвольное число в консоле
Ввести пограничное число в консоле

Если 1-ое число меньше пограничного, вывести сообщение об этом.
Если 1-ое число больше пограничного, вывести сообщение об этом.
Если 1-ое число больше пограничного более, чем в 3 раза, сообщить об этом.
"""


def is_number(x):
    """
    Проверка является ли x числом.
    """
    try:
        float(x)
        return True
    except:
        return False


def main():
    """
    Главная функция.
    """
    input_number = input("Введите число: ")
    input_border = input("Введите пограничное число: ")

    # проверка на ввод числа
    if not (is_number(input_number) and is_number(input_border)):
        print("Вы должны ввести цифры для числа и для пограничного числа.")
        return 1

    # перевод строки в числа
    input_number = float(input_number)
    input_border = float(input_border)

    # проверка границы
    if input_number < input_border:
        print("Первое число меньше пограничного.")
    elif input_number > input_border:
        if input_number > input_border * 3:
            print("Первое число больше пограничного более, чем в три раза.")
            return 0
        print("Первое число больше пограничного.")

    return 0


if __name__ == "__main__":
    main()