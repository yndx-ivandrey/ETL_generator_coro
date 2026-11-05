Декоратор корутин без типизации:

```python
from functools import wraps


def coroutine(func):
    @wraps(func)
    def inner(*args, **kwargs):
        fn = func(*args, **kwargs)
        next(fn)
        return fn

    return inner
```

Для python 3.11 и ниже типизируем декоратор через ParamSpec и TypeVar

```python
from collections.abc import Callable, Generator
from functools import wraps
from typing import ParamSpec, TypeVar

F_Spec = ParamSpec("F_Spec")
Y = TypeVar("Y")
S = TypeVar("S")
R = TypeVar("R")


def coroutine(
    func: Callable[F_Spec, Generator[Y, S, R]],
) -> Callable[F_Spec, Generator[Y, S, R]]:
    @wraps(func)
    def inner(*args: F_Spec.args, **kwargs: F_Spec.kwargs) -> Generator[Y, S, R]:
        fn = func(*args, **kwargs)
        next(fn)
        return fn

    return inner
```

Начиная с версии 3.12, можно использовать дженерики:

```python
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
```