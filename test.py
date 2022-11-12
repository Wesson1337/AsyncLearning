from collections import namedtuple
from datetime import datetime

x = namedtuple('City', 'name country populations coordinates')

y = x('Tokyo', 'lol', 'lol', 'lol')
print(y.count('lol'))


def main(data_dict):
    match data_dict:
        case {"name": str(name), "access": 1 | 2 as access, "request": request}:
            print(f"Пользователь {name} получил доступ к функции {request} с правами {access}")
        case _:
            print("Неудача")


main({"name": "Daniil", "access": 1, "request": "save"})


from array import array
from random import random

start = datetime.now()

floats = array('d', (random() for i in range(10 ** 7)))
print(floats[-1])
fp = open('floats.bin', 'wb')
floats.tofile(fp)
fp.close()

floats2 = array('d')
fp = open('floats.bin', 'rb')
floats2.fromfile(fp, 10**7)
fp.close()
print(floats2[-1])

print(f'Array write and read - {datetime.now() - start}')

start = datetime.now()

floats_list = [random() for _ in range(10 ** 7)]
print(floats_list[-1])
f = open('floats_list.txt', 'w')
for number in floats_list:
    f.write(f'{str(number)}\n')
f.close()

floats_list2 = []
f = open('floats_list.txt', 'r')
for number in f.read().split('\n'):
    if number:
        float_number = float(number)
        floats_list2.append(float_number)
print(floats_list2[-1])
f.close()

print(f'List write and read - {datetime.now() - start}')
