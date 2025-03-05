
def coro():
    """Sample coroutine"""
    print("Начало работы корутины")
    val = yield
    print(f"В корутину пришло значение: {val}")
    yield val * 2
    print("Завершение работы корутины")


if __name__ == "__main__":
    c = coro()
    next(c)
    c.send(12)
    next(c)
