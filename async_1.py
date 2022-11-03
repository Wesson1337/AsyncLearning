from typing import Generator


def gen_send_method() -> Generator[None, int, str]:
    while True:
        item = 1
        y = yield item
        print(f"item={item}, y={y}")
        if item == 42:
            return 'hello'


if __name__ == '__main__':
    g = gen_send_method()
    next(g)
    next(g)
    g.send(2)
