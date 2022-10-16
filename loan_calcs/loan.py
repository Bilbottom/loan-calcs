"""

"""
import math
from enum import Enum, auto
from decimal import Decimal


# noinspection PyArgumentList
class InterestType(Enum):
    """Loan interest types."""
    CAPITAL_AND_INTEREST = auto()
    INTEREST_ONLY = auto()


# noinspection PyArgumentList
class RateType(Enum):
    """Loan rate types."""
    VARIABLE = auto()
    FIXED_REPAYMENT = auto()
    FIXED_PRINCIPAL = auto()


class InterestApplyMethod(Enum):
    """Whether the interest is applied before or after the repayment."""
    BEFORE = 0
    AFTER = 1


class Loan:
    """A loan.

    TODO: Consider adding subclasses for the different loan types.
    """
    def __init__(
        self, *,
        loan_amount: float = None,
        interest_rate: float = None,
        total_repayments: int = None,
        periodic_repayment: float = None,
        before_or_after: InterestApplyMethod = InterestApplyMethod.BEFORE
    ):
        """Create a Loan object."""
        args = [loan_amount, interest_rate, total_repayments, periodic_repayment]
        if (non_nulls := sum(arg is None for arg in args)) != 1:
            raise AssertionError(
                f'There are {non_nulls} non-null arguments when there should be exactly 1.'
            )

        self.loan_amount = Decimal(str(loan_amount)) if loan_amount else None
        self.interest_rate = Decimal(str(interest_rate)) if interest_rate else None
        self.total_repayments = Decimal(str(total_repayments))
        self.periodic_repayment = Decimal(str(periodic_repayment)) if periodic_repayment else None
        self.before_or_after = Decimal(str(before_or_after.value))
        self.contract = Contract()

    def _amortised_rate(self, n: Decimal) -> Decimal:
        """Calculate the amortised rate at `n`.

        Let :math:`R` be the interest rate on the loan. Then the amortised rate is given by :math:`(1 + R)^{n}`.
        """
        if n < 0:
            raise AssertionError('The amortise rate period has to be positive.')
        return Decimal((self.interest_rate + Decimal(1)) ** n)

    @property
    def total_amortised_rate(self) -> Decimal:
        """Calculate the amortised rate at the complete term."""
        return Decimal(self._amortised_rate(self.total_repayments))

    def _calculate_loan_amount(self) -> Decimal:
        """Calculate the loan amount using the interest rate, total repayments, and period repayment.

        Let:
             * :math:`R`: Periodic interest rate.
             * :math:`N`: Total number of repayments.
             * :math:`P`: Periodic repayment.
             * :math:`b`: Whether the interest is applied before or after the repayment.

        Then the loan value, :math:`L`, is:
          .. math::
            P = \\frac{ PR^{b - 1}((1 + R)^{n} - 1) }{ (1 + R)^{n} }

        """
        return Decimal(
            round(
                self.periodic_repayment
                * (self.interest_rate ** (self.before_or_after - Decimal(1)))
                * (self.total_amortised_rate - Decimal(1))
                / self.total_amortised_rate,
                2
            )
        )

    def _calculate_periodic_repayment(self) -> Decimal:
        """Calculate the period repayment using the interest rate, total repayments, and loan amount.

        Let:
             * :math:`L`: Loan amount.
             * :math:`R`: Periodic interest rate.
             * :math:`N`: Total number of repayments.
             * :math:`b`: Whether the interest is applied before or after the repayment.

        Then the period repayment value, :math:`P`, is:
          .. math::
            P = \\frac{ LR^{1 - b}(1 + R)^{N} }{ (1 + R)^{N} - 1 }

        """
        return Decimal(
            round(
                (self.interest_rate ** (Decimal(1) - self.before_or_after))
                * self.loan_amount
                * self.total_amortised_rate
                / (self.total_amortised_rate - Decimal(1)),
                2
            )
        )

    def _calculate_total_instalments(self) -> int:
        """Calculate the total repayments using the interest rate, period repayment, and loan amount.

        This uses the natural log form of the equation instead of the log form. Let:
            * :math:`L`: Loan amount.
            * :math:`R`: Periodic interest rate.
            * :math:`P`: Periodic repayment.
            * :math:`b`: Whether the interest is applied before or after the repayment.

        Then the natural log form of the total instalments, :math:`N`, is:
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
        """Calculate the loan balance at :math:`period`.

        Let:
             * :math:`L`: Loan amount.
             * :math:`R`: Periodic interest rate.
             * :math:`b`: Whether the interest is applied before or after the repayment.
             * :math:`n`: The period.

        Then the balance at the end of period :math:`n`, :math:`b_{n}`, is:
          .. math::
            B_{n} = L(1 + R)^{n} - PR^{b - 1}((1 + R)^{n} - 1)

        """
        return Decimal(
            round(
                self.loan_amount * self._amortised_rate(period) - (
                    self.periodic_repayment
                    * (self.interest_rate ** self.before_or_after)
                    * (self._amortised_rate(period) - Decimal(1))
                ),
                2
            )
        )


class Contract:
    """A loan contract. Defines the repayment types and schedule."""
    def __init__(
        self,
        interest_type: InterestType = InterestType.CAPITAL_AND_INTEREST,
        number_of_holiday_repayments: int = 0
    ):
        """Define a Loan contract."""
        pass


class Amortiser:
    """Calculations over the amortisation schedule."""
    def __init__(self):
        pass


class Repayment:
    """A loan repayment."""
    def __init__(self):
        pass
