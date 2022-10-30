"""
Similar packages:
* https://loan-calculator.readthedocs.io/en/latest/index.html
* https://mortgage.readthedocs.io/en/latest/index.html
"""
from dataclasses import dataclass
from decimal import Decimal
import json
from typing import Protocol

from loan_calcs.loan import (
    Loan,
    InterestRateType,
    RepaymentType,
    FixedRepaymentLoan,
    FixedPrincipalLoan,
    InterestOnlyLoan
)


def pprint(json_text: str | dict, indent: int = 4) -> None:
    """Pretty print JSON/dict objects."""
    if isinstance(json_text, str):
        json_text = json.loads(json_text)

    try:
        print(
            json.dumps(
                json_text,
                sort_keys=True,
                indent=indent,
                separators=(',', ': '),
                cls=MyEncoder,
            )
        )
    except TypeError as e:
        print(repr(e))
        print(json_text)


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        return repr(obj)


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


def print_loan_details(loan_example: LoanExample) -> None:
    """Print some loan details. Development only."""
    properties = [
        'loan_amount',
        'interest_rate',
        'total_repayments',
        # 'fixed_periodic_repayment',
    ]
    loan: Loan = create_loan(loan_example)
    details: dict = {key: loan.__dict__[key] for key in properties}
    details['balance_at_20'] = loan.calculate_balance_at_period(period=20)
    details['interest_at_20'] = loan.calculate_repayment_interest_at_period(period=20)
    details['principal_at_20'] = loan.calculate_repayment_principal_at_period(period=20)
    pprint(details)


def main() -> None:
    """Entry point into this project."""
    fixed_repayment_example = LoanExample(
        loan_amount=100_000,
        interest_rate=0.075,
        total_repayments=100,
        interest_rate_type=InterestRateType.VARIABLE,
        repayment_type=RepaymentType.FIXED_REPAYMENT,
    )
    fixed_principal_example = LoanExample(
        loan_amount=100_000,
        interest_rate=0.075,
        total_repayments=100,
        interest_rate_type=InterestRateType.VARIABLE,
        repayment_type=RepaymentType.FIXED_PRINCIPAL,
    )
    interest_only_example = LoanExample(
        loan_amount=100_000,
        interest_rate=0.075,
        total_repayments=100,
        interest_rate_type=InterestRateType.VARIABLE,
        repayment_type=RepaymentType.INTEREST_ONLY,
    )

    print_loan_details(fixed_repayment_example)
    # print_loan_details(fixed_principal_example)
    # print_loan_details(interest_only_example)


if __name__ == '__main__':
    main()
