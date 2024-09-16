import warnings
import inspect
from functools import wraps


__version__ = '1.20240916'


class DeprecatedError(Exception):
    pass


def deprecated(func):
    """
    This mimics Java's deprecation annotation. There this RAISES the error
    error: If True
    """
    @wraps(func)
    def deprecate_function(*args, **kwargs):
        raise DeprecatedError('{}() is deprecated'.format(func.__name__))

    return deprecate_function


class Deprecated:
    def __init__(self, reason=None):
        self.reason = reason if reason else "Reason for deprecation was not given"

    def __call__(self, cls_or_func):
        if inspect.isfunction(cls_or_func):
            _code = cls_or_func.__code__
            fmt = "{name} is a deprecated function! ({reason})."
            filename = _code.co_filename
            line_number = _code.co_firstlineno + 1

        elif inspect.isclass(cls_or_func):
            fmt = "{name} is a deprecated class! ({reason})."
            filename = cls_or_func.__module__
            line_number = 1

        else:
            raise TypeError(type(cls_or_func))

        message = fmt.format(name=cls_or_func.__name__, reason=self.reason)

        @wraps(cls_or_func)
        def new_func(*args, **kwargs):
            # Ensure that the warning is seen
            with warnings.catch_warnings():
                warnings.simplefilter("always", DeprecationWarning)
                warnings.warn_explicit(
                    message,
                    category=DeprecationWarning,
                    filename=filename,
                    lineno=line_number,
                )
            return cls_or_func(*args, **kwargs)

        return new_func
