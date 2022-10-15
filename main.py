"""
Similar packages:
* https://loan-calculator.readthedocs.io/en/latest/index.html
* https://mortgage.readthedocs.io/en/latest/index.html
"""
from decimal import Decimal

from loan_calcs.loan import Loan


def main() -> None:
    loan = Loan(loan_amount=100_000, interest_rate=0.075, total_repayments=240)
    print(loan._calculate_periodic_repayment())
    # print(loan.calculate_balance(period=0))


if __name__ == '__main__':
    main()
