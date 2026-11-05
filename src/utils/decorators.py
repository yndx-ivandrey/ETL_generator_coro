from collections.abc import Callable, Generator
from functools import wraps


def coroutine[Y, S, R, **P](
    func: Callable[P, Generator[Y, S, R]],
) -> Callable[P, Generator[Y, S, R]]:
    @wraps(func)
    def inner(*args: P.args, **kwargs: P.kwargs) -> Generator[Y, S, R]:
        fn = func(*args, **kwargs)
        next(fn)
        return fn

    return inner
