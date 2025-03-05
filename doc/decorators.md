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

Для python 3.11 и ниже типизируем декоратор через ParamSpec

```python
from functools import wraps
from typing import Any, Callable, Generator, ParamSpec

F_Spec = ParamSpec("F_Spec")


def coroutine(
    func: Callable[F_Spec, Generator[Any, Any, Any]],
) -> Callable[F_Spec, Generator[Any, Any, Any]]:
    @wraps(func)
    def inner(*args: F_Spec.args, **kwargs: F_Spec.kwargs) -> Generator[Any, Any, Any]:
        fn = func(*args, **kwargs)
        next(fn)
        return fn

    return inner
```

Начиная с версии 3.12 можно использовать дженерики:

```python
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

```