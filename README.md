loan-calcs
---

Classes for creating loans and their key properties.


## Notation
A _loan_ is a fixed value of money borrowed by an entity and usually repaid over a series of instalments.

The following notation is used throughout this project for loans:

- `L`: Loan amount
- `R`: Periodic interest rate
- `N`: Total number of repayments
- `P_n`: Total periodic repayment value at period `n`
- `P_{P, n}`: The principal part of the periodic repayment value at period `n`
- `P_{I, n}`: The interest part of the periodic repayment value at period `n`
- `b`: Whether the interest is applied before or after the repayment
- `B_n`: The balance on the loan at period `n`

The repayment for a loan, `P_n`, is split into 2 components:
- The _principal_ part, `P_{P, n}`, which is paying off the original money that was borrowed.
- The _interest_ part, `P_{I, n}`, which is paying off the interest applied on the loan.

In 'real life', a loan can have other components such as fees. These are outside the scope of this project.


## Calculations

Many of the properties are calculated analytically. The calculations are described in the `tex/proofs.pdf` file.
