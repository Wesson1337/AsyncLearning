from collections import namedtuple

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
