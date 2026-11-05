from collections.abc import Generator, Iterable, Iterator


def fib_fn(n: int) -> list[int]:
    if n <= 0:
        return []
    if n == 1:
        return [0]
    fib = [0, 1]
    for _ in range(2, n):
        fib.append(fib[-1] + fib[-2])
    return fib


class FibIterable:
    def __init__(self, count: int) -> None:
        self.count = count

    def __iter__(self) -> Iterator[int]:
        return FibIterator(self.count)


class FibIterator:
    def __init__(self, count: int):
        self.count = count
        self.a = 0
        self.b = 1

    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        if not self.count:
            raise StopIteration()
        current = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count -= 1
        return current


def fib_gen(n: int) -> Iterator[int]:
    a, b = 0, 1
    counter = 0
    while counter < n:
        yield a
        counter += 1
        a, b = b, a + b


# def gen_func(i: int):
#     if True:
#         return
#     yield i


if __name__ == "__main__":
    print(fib_fn(10))
    print([i for i in FibIterable(10)])
    print(f"{issubclass(FibIterable, Iterable)=}")
    print(f"{issubclass(FibIterable, Iterator)=}")
    it = iter(FibIterable(10))
    print(f"{isinstance(it, Iterator)=}")
    print([i for i in fib_gen(10)])

    a = (i for i in fib_gen(10))
    print(type(a))
    print(f"{isinstance(a, Iterator)=}")
    print(f"{isinstance(a, Iterable)=}")
    print(f"{isinstance(a, Generator)=}")
