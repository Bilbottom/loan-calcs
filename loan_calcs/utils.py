"""
All handy enums and module functions that can be used throughout the package.
"""
from __future__ import annotations

import decimal
import enum
import functools
from typing import Any, Callable


# noinspection PyArgumentList
class RepaymentType(enum.Enum):
    """
    Loan repayment types which determines the values of each repayment.

    Check the documentation of the corresponding loan objects for explanations
    of their differences.
    """
    FIXED_REPAYMENT = enum.auto()
    FIXED_PRINCIPAL = enum.auto()
    INTEREST_ONLY = enum.auto()


# noinspection PyArgumentList
class InterestRateType(enum.Enum):
    """
    Loan interest rate types.

    - VARIABLE: A variable rate can change over the lifetime of the loan. This
      is usually when the interest rate is tied to a benchmark rate that also
      changes over time, such as the Bank of England rate.

    - FIXED: A fixed rate does not change over the lifetime of the loan.
    """
    VARIABLE = enum.auto()
    FIXED = enum.auto()


class InterestApplyMethod(enum.Enum):
    """
    Whether the interest is applied before or after the repayment.
    """
    BEFORE = 0
    AFTER = 1


def _to_decimal(value: Any) -> decimal.Decimal:
    """
    Casting a float directly to a decimal messes with the precision so casting
    to a string first is preferable.
    """
    # Purposely pass None into Decimal to generate the correct error
    return Decimal(None) if value is None else decimal.Decimal(str(value))  # noqa


def _decimal(round_to: int | None = None) -> Callable:
    """
    Decorator for the `_to_decimal` function with an optional precision to round
    to.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if round_to is None:
                return _to_decimal(func(*args, **kwargs))
            else:
                return _to_decimal(round(func(*args, **kwargs), round_to))
        return wrapper
    return decorator


def _calculate_amortised_rate(interest_rate: decimal.Decimal, n: decimal.Decimal) -> decimal.Decimal:
    """
    Calculate the amortised rate at `n`.

    Let :math:`R` be the interest rate on a loan. Then the amortised rate is
    given by :math:`(1 + R)^{n}`.
    """
    if n < 0:
        raise AssertionError("The amortise rate period has to be positive.")
    return _to_decimal((decimal.Decimal(1) + interest_rate) ** n)
