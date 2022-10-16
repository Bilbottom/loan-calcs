
DROP TABLE IF EXISTS loan_accounts;
DROP TABLE IF EXISTS loan_repayments;


CREATE TABLE loan_accounts(
    account_id                   TEXT NOT NULL PRIMARY KEY,
    product                      TEXT,
    product_description          TEXT,
    loan_amount                  REAL,
    total_term                   INTEGER,
    total_rate                   REAL,
    base_rate                    REAL,
    margin_rate                  REAL,
    spread_rate                  REAL,
    start_date                   DATE,
    maturity_date                DATE,
    accrued_interest             REAL,
    number_of_holiday_repayments INTEGER,
    number_of_capital_repayments INTEGER
);

CREATE TABLE loan_repayments(
    account_id            TEXT NOT NULL REFERENCES loan_accounts(account_id),
    repayment_number      INTEGER,
    repayment_date        DATE,
    total_installment     REAL,
    principal_installment REAL,
    interest_installment  REAL,
    tax_installment       REAL,
    charge_amount         REAL,
    CONSTRAINT loan_repayments_pk PRIMARY KEY (account_id, repayment_number)
);


/* loan_accounts */
INSERT INTO loan_accounts(
    account_id,
    product,
    product_description,
    loan_amount,
    total_term,
    total_rate,
    base_rate,
    margin_rate,
    spread_rate,
    start_date,
    maturity_date,
    accrued_interest,
    number_of_holiday_repayments,
    number_of_capital_repayments
)
SELECT DISTINCT
    account_id,
    product,
    product_description,
    loan_initial_balance,
    loan_total_term,
    loan_total_rate,
    loan_base_rate,
    loan_margin_rate,
    loan_spread_rate,
    loan_start_date,
    loan_maturity_date,
    accrued_interest,
    number_of_holiday_repayments,
    number_of_capital_repayments
FROM raw__loan_examples
;


/* loan_repayments */
INSERT INTO loan_repayments(
    account_id,
    repayment_number,
    repayment_date,
    total_installment,
    principal_installment,
    interest_installment,
    tax_installment,
    charge_amount
)
SELECT DISTINCT
    account_id,
    repayment_number,
    repayment_date,
    total_installment,
    principal_installment,
    interest_installment,
    tax_installment,
    charge_amount
FROM raw__loan_examples
;
