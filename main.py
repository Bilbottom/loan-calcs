"""
Similar packages:
* https://loan-calculator.readthedocs.io/en/latest/index.html
* https://mortgage.readthedocs.io/en/latest/index.html
"""
from decimal import Decimal
from typing import Protocol
from dataclasses import dataclass

from loan_calcs.loan import (
    Loan,
    InterestRateType,
    RepaymentType,
    FixedRepaymentLoan,
    FixedPrincipalLoan,
    InterestOnlyLoan
)


@dataclass
class LoanExample:
    loan_amount: float
    interest_rate: float
    total_repayments: int
    interest_rate_type: InterestRateType
    repayment_type: RepaymentType


def create_loan(loan_object: LoanExample) -> Loan:
    """Create a Loan object from a dictionary which has the corresponding properties. Development only."""
    loan_types = {
        RepaymentType.FIXED_REPAYMENT: FixedRepaymentLoan,
        RepaymentType.FIXED_PRINCIPAL: FixedPrincipalLoan,
        RepaymentType.INTEREST_ONLY: InterestOnlyLoan,
    }
    return loan_types[loan_object.repayment_type](
        loan_amount=loan_object.loan_amount,
        interest_rate=loan_object.interest_rate,
        total_repayments=loan_object.total_repayments
    )


def main() -> None:
    """Entry point into this project."""
    fixed_repayment_example = LoanExample(
        loan_amount=100_000,
        interest_rate=0.075,
        total_repayments=240,
        interest_rate_type= InterestRateType.VARIABLE,
        repayment_type= RepaymentType.FIXED_REPAYMENT,
    )
    interest_only_example = LoanExample(
        loan_amount=117_000,
        interest_rate=0.06,
        total_repayments=60,
        interest_rate_type= InterestRateType.VARIABLE,
        repayment_type= RepaymentType.INTEREST_ONLY,
    )

    loan = create_loan(fixed_repayment_example)
    print(loan.__dict__)
    print(loan._calculate_periodic_repayment())
    # print(loan.calculate_balance(period=0))


if __name__ == '__main__':
    main()
