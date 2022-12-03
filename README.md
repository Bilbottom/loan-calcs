loan-calcs
---

Classes for creating loans and their key properties.


## Notation
A _loan_ is a fixed value of money borrowed by an entity and usually repaid over a series of instalments.

The following notation is used throughout this project for loans:

- `L`: Loan amount.
- `R`: Periodic interest rate.
- `N`: Total number of repayments.
- `P`: Total periodic repayment value (the principal part has a subscript `p`, `P_{p}`).
- `b`: Whether the interest is applied before or after the repayment.
- `B_n`: The balance on the loan at period `n`.

The repayment for a loan typically has (at least) 2 components:
- The _principal_ part, which is paying off the original money that was borrowed.
- The _interest_ part, which is paying off the interest applied on the loan.

In 'real life', a loan can have other components such as fees. These are outside the scope of these objects. Note that any of these can be zero.


## Calculations

Many of the properties are calculated analytically. The calculations are described in the `proofs.pdf` file.

