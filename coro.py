def coro():
    print("Начало работы корутины")
    val = yield
    print(f"В корутину пришло значение: {val}")
    yield val * 2
    print("Завершение работы корутины")


def coro2():
    val = "initial"
    while True:
        try:
            val = yield f"yield {val=}"
            print(f"received {val}")
        except GeneratorExit:
            print("oops")
            raise
        except IndexError as e:
            print(e)
        if val is None:
            break


def coro3():
    print("start coro3")
    yield from coro2()
    print("stop coro3")


if __name__ == "__main__":
    c = coro()
    next(c)
    c.send(12)
    next(c)
