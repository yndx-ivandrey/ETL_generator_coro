from functools import wraps
from typing import Any, Callable, Generator


def coroutine[**P](
    func: Callable[P, Generator[Any, Any, Any]],
) -> Callable[P, Generator[Any, Any, Any]]:
    @wraps(func)
    def inner(*args: P.args, **kwargs: P.kwargs) -> Generator[Any, Any, Any]:
        fn = func(*args, **kwargs)
        next(fn)
        return fn

    return inner
