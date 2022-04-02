"""
3.
Написать мини калькулятор.
В консоле ожидается ввод того сивола, операцию которую мы будем выполнять.
Операции: +, -, /, *, возведение в степень, модуль, рандомное число,
факториал и арккосинус.
В консоль вводится столько значений, сколько требуется для операции.
Для рандомного например 0.
Выводим значение.
"""
import math
import random
import typing


class Operation:

    __slots__ = ('label', 'nums', 'func')

    def __init__(self, label: str, nums: int, func: typing.Callable) -> None:
        self.label = label
        self.nums = nums
        self.func = func

    def input_num(self):

        def is_num(x) -> bool:
            try:
                float(x)
                return True
            except Exception:
                return False

        values = []
        i = 1
        while len(values) != self.nums:
            tmp = input('Введите ' + str(i) + '-ое число: ')
            if not is_num(tmp):
                print('Вы ввели не число.')
            else:
                values.append(float(tmp))
                i = i + 1
        return values

    def count(self, values):
        if values == [] and self.nums != 0:
            return
        return self.func(*values)


def main():
    OPERATIONS = (
        Operation(label='+', nums=2, func=lambda x, y: x + y),
        Operation(label='-', nums=2, func=lambda x, y: x - y),
        Operation(label='*', nums=2, func=lambda x, y: x * y),
        Operation(label='/', nums=2, func=lambda x, y: x / y),
        Operation(label='**', nums=2, func=lambda x, y: x**y),
        Operation(label='mod', nums=1, func=lambda x: abs(x)),
        Operation(label='random', nums=0, func=lambda: random.random()),
        Operation(label='!', nums=1, func=lambda x: math.factorial(x)),
        Operation(label='acos', nums=1, func=lambda x: math.acos(x)),
    )
    OPERATIONS_TYPES = [x.label for x in OPERATIONS]

    print('Виды операций:', ''.join([x + ', ' for x in OPERATIONS_TYPES])[:-2])
    input_operation = input('Введите тип операции: ')

    if input_operation not in OPERATIONS_TYPES:
        print('Введена неправильная операция.')
        return 1

    operation = OPERATIONS[OPERATIONS_TYPES.index(input_operation)]
    nums = operation.input_num()
    result = operation.count(nums)
    print("Итог:", result)


if __name__ == "__main__":
    main()
