"""
2.
Ввести произвольную строку в консоль.
Циклом пройтись по всем символам этой строки
Пропустить 3-й символ.
Если есть символ "c" вывести сообщение об этом.
Загуглить функцию вывода длины строки.
Не выводить последний символ в строке.
"""
from duckduckgo_search import ddg


def googling(keywords: str):
    try:
        res = ddg(keywords)
        if len(res) > 0:
            return res[0]
        else:
            return None
    except Exception:
        return None


def main():
    input_value = input('Введите произвольную строку: ')
    for i in range(0, len(input_value), 1):
        if i == 2:
            continue
        if input_value[i] in ["c", "с"]:
            print('В произвольной строке присутствует символ "c".')

    print("\nМы гуглим")
    result = googling("python str length")

    if result:
        print('\nВот, что мы нашли:')
        print('Название:', result['title'])
        print('Ссылка:', result['href'])
        print('Информация:', result['body'], '\n')
    else:
        print('Гуглинг не удался...')

    print('Произвольная строка без послденего символа:', input_value[:-1])


if __name__ == "__main__":
    main()
