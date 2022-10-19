"""
All handy enums and module functions that can be used throughout the package.
"""
from enum import Enum, auto
from functools import wraps
from typing import Any, Callable
from decimal import Decimal


# noinspection PyArgumentList
class RepaymentType(Enum):
    """Loan repayment types which determines the values of each repayment.

    Check the documentation of the corresponding loan objects for explanations of their differences.
    """
    FIXED_REPAYMENT = auto()
    FIXED_PRINCIPAL = auto()
    INTEREST_ONLY = auto()


# noinspection PyArgumentList
class InterestRateType(Enum):
    """Loan interest rate types.

    VARIABLE
    ---
    A variable rate can change over the lifetime of the loan. This is usually when the interest rate is tied to a
    benchmark rate that also changes over time, such as the Bank of England rate.

    FIXED
    ---
    A fixed rate does not change over the lifetime of the loan.
    """
    VARIABLE = auto()
    FIXED = auto()


class InterestApplyMethod(Enum):
    """Whether the interest is applied before or after the repayment."""
    BEFORE = 0
    AFTER = 1


def _to_decimal(value: Any) -> Decimal:
    """Casting a float directly to a decimal messes with the precision so casting to a string first is preferable."""
    # sourcery skip: assign-if-exp, reintroduce-else
    if value is None:
        # Purposely pass None into Decimal to generate the correct error
        return Decimal(None)  # noqa
    return Decimal(str(value))


def decimal(round_to: int = None) -> Callable:
    """Decorator for the `_to_decimal` function with an optional precision to round to."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if round_to is None:
                return _to_decimal(func(*args, **kwargs))
            else:
                return _to_decimal(round(func(*args, **kwargs), round_to))
        return wrapper
    return decorator


def _calculate_amortised_rate(interest_rate: Decimal, n: Decimal) -> Decimal:
    """Calculate the amortised rate at `n`.

    Let :math:`R` be the interest rate on a loan. Then the amortised rate is given by :math:`(1 + R)^{n}`.
    """
    if n < 0:
        raise AssertionError('The amortise rate period has to be positive.')
    return _to_decimal((Decimal(1) + interest_rate) ** n)
