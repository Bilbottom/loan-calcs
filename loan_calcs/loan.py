"""

"""
import math
from abc import ABC, abstractmethod
from enum import Enum, auto
from decimal import Decimal
from typing import Protocol, Any

from .repayment_frequency import RepaymentFrequency


# noinspection PyArgumentList
class RepaymentType(Enum):
    """Loan repayment types which determines the values of each repayment.

    `FIXED_REPAYMENT`
    ---
    A fixed repayment loan is the 'normal' type of loan: each repayment pays off some original loan amount but also some
    interest. Each repayment has the same value.

    `FIXED_PRINCIPAL`
    ---
    A fixed principal loan is similar to a fixed repayment loan where each repayment pays off some original loan amount
    and also some interest. However, only the principal part of each repayment has the same value.

    `INTEREST_ONLY`
    ---
    An interest-only loan is where each periodic repayment only pays off the accrued interest on the loan. The principal
    value of the loan is paid off in the final repayment.
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
    """Casting a float to a decimal does not preserve the precision so casting to a string first is preferable."""
    # sourcery skip: assign-if-exp, reintroduce-else
    if value is None:
        # Purposely pass None into Decimal to generate the correct error
        return Decimal(None)  # noqa
    return Decimal(str(value))


def _calculate_amortised_rate(interest_rate: Decimal, n: Decimal) -> Decimal:
    """Calculate the amortised rate at `n`.

    Let :math:`R` be the interest rate on the loan. Then the amortised rate is given by :math:`(1 + R)^{n}`.
    """
    if n < 0:
        raise AssertionError('The amortise rate period has to be positive.')
    return _to_decimal((interest_rate + Decimal(1)) ** n)


class Loan(ABC):
    """A loan, which is a fixed value of money borrowed by an entity and usually repaid over a series of instalments.

    The following notation is used throughout the Loan classes:
         * :math:`L`: Loan amount.
         * :math:`R`: Periodic interest rate.
         * :math:`N`: Total number of repayments.
         * :math:`P`: Periodic repayment value (total value).
         * :math:`b`: Whether the interest is applied before or after the repayment.
         * :math:`B_n`: The balance on the loan at period :math:`n`.
    """
    def __init__(
        self, *,
        loan_amount: float = None,
        interest_rate: float = None,
        total_repayments: int = None,
        periodic_repayment: float = None,
        before_or_after: InterestApplyMethod = InterestApplyMethod.BEFORE
    ) -> None:
        """Create a loan."""
        self.loan_amount: Decimal = _to_decimal(loan_amount)
        self.interest_rate: Decimal = _to_decimal(interest_rate)
        self.total_repayments: Decimal = _to_decimal(total_repayments)
        self.periodic_repayment: Decimal = _to_decimal(periodic_repayment)
        self.before_or_after = before_or_after.value

    @property
    def total_amortised_rate(self) -> Decimal:
        """Calculate the amortised rate at the complete term."""
        return _calculate_amortised_rate(self.interest_rate, self.total_repayments)

    @abstractmethod
    def _calculate_loan_amount(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_periodic_repayment(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_total_instalments(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_balance(self, period: int) -> Decimal:
        """Calculate the loan balance, :math:`B_{n}`, at the end of period :math:`n`."""
        pass


class FixedRepaymentLoan(Loan):
    """A fixed repayment loan."""
    _type: RepaymentType = RepaymentType.FIXED_REPAYMENT

    def __init__(
        self, *,
        loan_amount: float = None,
        interest_rate: float = None,
        total_repayments: int = None,
        periodic_repayment: float = None,
        before_or_after: InterestApplyMethod = InterestApplyMethod.BEFORE
    ):
        """Create a fixed repayment loan.

        A fixed repayment loan has 4 key properties and can be defined by exactly 3 of them:
            * The loan amount
            * The interest rate
            * The number of repayments
            * The repayment value

        With any 3, the 4th can be determined.

        """
        super().__init__(
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            total_repayments=total_repayments,
            periodic_repayment=periodic_repayment,
            before_or_after=before_or_after
        )

    def _calculate_loan_amount(self) -> Decimal:
        """Calculate the loan amount (:math:`L`) using the interest rate (:math:`R`), total repayments (:math:`N`), the
        period repayment (:math:`P`), and whether the interest is applied before or after the repayment (:math:`b`).

        The loan value, :math:`L`, for a fixed repayment loan is:
          .. math::
            P = \\frac{ PR^{b - 1}((1 + R)^{n} - 1) }{ (1 + R)^{n} }

        """
        return _to_decimal(
            round(
                self.periodic_repayment
                * (self.interest_rate ** (self.before_or_after - Decimal(1)))
                * (self.total_amortised_rate - Decimal(1))
                / self.total_amortised_rate,
                2
            )
        )

    def _calculate_periodic_repayment(self) -> Decimal:
        """Calculate the period repayment (:math:`P`) using the interest rate (:math:`R`), total repayments (:math:`N`),
        loan amount (:math:`L`), and whether the interest is applied before or after the repayment (:math:`b`).

        The period repayment value, :math:`P`, for a fixed total repayment value is:
          .. math::
            P = \\frac{ LR^{1 - b}(1 + R)^{N} }{ (1 + R)^{N} - 1 }

        For an interest-only loan, the periodic repayment is the same as the periodic interest so that:
          .. math::
            P = LR

        In this case, the final repayment is then :math:`P + L`.

        For the fixed principal loan, we could have 2 scenarios:
            1. The periodic principal is the loan value divided by the number of repayments
            2. The periodic principal is some fixed amount, with the difference added on the final repayment (the balloon)

        """
        return _to_decimal(
            round(
                (self.interest_rate ** (Decimal(1) - self.before_or_after))
                * self.loan_amount
                * self.total_amortised_rate
                / (self.total_amortised_rate - Decimal(1)),
                2
            )
        )

    def _calculate_total_instalments(self) -> int:
        """Calculate the total repayments (:math:`N`) using the interest rate (:math:`R`), period repayment (:math:`R`),
        loan amount (:math:`L`), and whether the interest is applied before or after the repayment (:math:`b`).

        The natural log form of the calculation for the total instalments, :math:`N`, of a fixed repayment loan is:
          .. math::
            N = \\frac{ \\ln(P / (P - LR^{1 - b}) }{ \\ln(1 + R) }

        The expression :math:`P - LR^{1 - b}` has to be strictly positive, otherwise there would be an unbounded number
        of instalments.

        """
        denominator = Decimal(
            self.periodic_repayment
            - self.loan_amount
            * self.interest_rate ** (Decimal(1) - self.before_or_after)
        )

        if denominator <= 0:
            # return math.inf
            raise ValueError(
                'The values of the loan amount, interest rate, and periodic repayment lead to an unbounded number of'
                ' instalments.'
            )
        else:
            return math.ceil(
                math.log(self.periodic_repayment / denominator)
                / math.log(self.interest_rate + Decimal(1))
            )

    def calculate_balance(self, period: Decimal) -> Decimal:
        """Calculate the loan balance, :math:`B_{n}`, at the end of period :math:`n`.

        The balance at the end of period :math:`n`, :math:`b_{n}`, for a fixed repayment loan is:
          .. math::
            B_{n} = L(1 + R)^{n} - PR^{b - 1}((1 + R)^{n} - 1)

        """
        return Decimal(
            round(
                self.loan_amount * _calculate_amortised_rate(self.interest_rate, period) - (
                    self.periodic_repayment
                    * (self.interest_rate ** self.before_or_after)
                    * (_calculate_amortised_rate(self.interest_rate, period) - Decimal(1))
                ),
                2
            )
        )


class FixedPrincipalLoan(Loan):
    """A fixed principal loan."""
    _type: RepaymentType = RepaymentType.FIXED_PRINCIPAL

    def __init__(
        self, *,
        loan_amount: float = None,
        interest_rate: float = None,
        total_repayments: int = None,
        periodic_repayment: float = None,
        before_or_after: InterestApplyMethod = InterestApplyMethod.BEFORE
    ):
        """Create a fixed principal loan.

        TODO: Determine whether the below is still correct or not.
        A fixed repayment loan has 4 key properties and can be defined by exactly 3 of them:
            * The loan amount
            * The interest rate
            * The number of repayments
            * The repayment value

        With any 3, the 4th can be determined.

        """
        super().__init__(
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            total_repayments=total_repayments,
            periodic_repayment=periodic_repayment,
            before_or_after=before_or_after
        )

    def _calculate_loan_amount(self) -> Decimal:
        """Calculate the loan amount (:math:`L`) using the interest rate (:math:`R`), total repayments (:math:`N`), the
        period repayment (:math:`P`), and whether the interest is applied before or after the repayment (:math:`b`).

        The loan value, :math:`L`, for a fixed principal loan is:
          .. math::
            P = <formula here>

        """
        pass

    def _calculate_periodic_repayment(self) -> Decimal:
        """Calculate the period repayment (:math:`P`) using the interest rate (:math:`R`), total repayments (:math:`N`),
        loan amount (:math:`L`), and whether the interest is applied before or after the repayment (:math:`b`).

        The period repayment value, :math:`P`, for a fixed principal loan is:
          .. math::
            P = <formula here>

        Note that, for the fixed principal loan, we could have 2 scenarios:
            1. The periodic principal is the loan value divided by the number of repayments
            2. The periodic principal is some fixed amount, with the difference added on the final repayment (the balloon)

        """
        pass

    def _calculate_total_instalments(self) -> int:
        """Calculate the total repayments (:math:`N`) using the interest rate (:math:`R`), period repayment (:math:`R`),
        loan amount (:math:`L`), and whether the interest is applied before or after the repayment (:math:`b`).

        The natural log form of the calculation for the total instalments, :math:`N`, of a fixed principal loan is:
          .. math::
            N = <formula here>

        """
        pass

    def calculate_balance(self, period: Decimal) -> Decimal:
        """Calculate the loan balance, :math:`B_{n}`, at the end of period :math:`n`.

        The balance at the end of period :math:`n`, :math:`b_{n}`, for a fixed principal loan is:
          .. math::
            B_{n} = <formula here>

        """
        pass


class InterestOnlyLoan(Loan):
    """A fixed principal loan."""
    _type: RepaymentType = RepaymentType.INTEREST_ONLY

    def __init__(
        self, *,
        loan_amount: float = None,
        interest_rate: float = None,
        total_repayments: int = None,
        periodic_repayment: float = None,
        before_or_after: InterestApplyMethod = InterestApplyMethod.BEFORE
    ):
        """Create an interest-only loan.

        TODO: Determine whether the below is still correct or not.
        A fixed repayment loan has 4 key properties and can be defined by exactly 3 of them:
            * The loan amount
            * The interest rate
            * The number of repayments
            * The repayment value

        With any 3, the 4th can be determined.

        """
        super().__init__(
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            total_repayments=total_repayments,
            periodic_repayment=periodic_repayment,
            before_or_after=before_or_after
        )

    def _calculate_loan_amount(self) -> Decimal:
        """Calculate the loan amount (:math:`L`) using the interest rate (:math:`R`), total repayments (:math:`N`), the
        period repayment (:math:`P`), and whether the interest is applied before or after the repayment (:math:`b`).

        The loan value, :math:`L`, for an interest-only loan is:
          .. math::
            P = <formula here>

        """
        pass

    def _calculate_periodic_repayment(self) -> Decimal:
        """Calculate the period repayment (:math:`P`) using the interest rate (:math:`R`), total repayments (:math:`N`),
        loan amount (:math:`L`), and whether the interest is applied before or after the repayment (:math:`b`).

        The period repayment value, :math:`P`, for an interest-only loan is:
          .. math::
            P = <formula here>

        """
        pass

    def _calculate_total_instalments(self) -> int:
        """Calculate the total repayments (:math:`N`) using the interest rate (:math:`R`), period repayment (:math:`R`),
        loan amount (:math:`L`), and whether the interest is applied before or after the repayment (:math:`b`).

        The total instalments, :math:`N`, for an interest-only loan is:
          .. math::
            N = <formula here>

        """
        pass

    def calculate_balance(self, period: Decimal) -> Decimal:
        """Calculate the loan balance, :math:`B_{n}`, at the end of period :math:`n`.

        The balance at the end of period :math:`n`, :math:`b_{n}`, for an interest-only loan is:
          .. math::
            B_{n} = <formula here>

        """
        pass
