"""
4.
Вводим 3 произвольных слова, например, название овощей.
Выводим все 3 слова в нижнем регистре, в верхнем регистре,
потом только первый символ в верхнем (есть отдельная функция для этого).
Далее вводим количество каждого овоща.
С помощью метода format выводим все данные в читаемом виде.
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
    vegetables = {}
    for i in range(1,4,1):
        name = input('Введите название {0}-ого овоща: '.format(i))
        vegetables.update({name:0})

    for x in vegetables.keys():
        print('Овощ:',x.lower())
    
    for x in vegetables.keys():
        print('Овощ:',x.upper())
    
    for x in vegetables.keys():
        print('Овощ:',x.title())

    for key in vegetables.keys():
        while True:
            value = input('Введите количество овоща "{0}": '.format(key))
            if is_number(value):
                break 
            else:
                print('Вы должны ввести число!')
        vegetables[key] = value
    
    for key, value in vegetables.items():
        print('Овощ - "{0}", количество - {1}'.format(key, value))

if __name__ == '__main__':
    main()
