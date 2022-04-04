"""
input содержит корректное
приглашение для ввода;

Задача 10. Яма

Что нужно сделать

Вы пишите компьютерную игру с
текстовой графикой, вам поручили
написать генеретор ландшафта,

Напишите программу которая получает на
вход число N и выводит на экран числа в
сиде "ямы" вот так:

5
5........5
54......45
543....345
5432..2345
5432112345
"""


def main():
    N = int(input())

    if N <= 0:
        return

    max_length = 0
    for i in range(1, N + 1, 1):
        max_length += len(str(i))
    max_length *= 2

    msg = ""
    for i in range(1, N + 1, 1):
        normal_line = ''
        reversed_line = ''
        for j in range(N, i - 1, -1):
            tmp = str(j)
            normal_line = normal_line + tmp
            reversed_line = tmp + reversed_line
        dots = '.' * (max_length - len(normal_line) * 2)
        msg = normal_line + dots + reversed_line + '\n' + msg

    print(msg, end='')


if __name__ == '__main__':
    main()
