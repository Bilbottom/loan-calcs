
/* Loan Accounts */
SELECT *
FROM loan_accounts
;


/* Loan Products */
SELECT
    product,
    product_description,
    account_id
FROM loan_accounts
GROUP BY
    product_description,
    product
ORDER BY
    product_description,
    product
;


/* Fixed Principal Loan Products */
SELECT
    la.product,
--     la.product_description,
    la.account_id,
    la.loan_amount,
    la.loan_amount / lr.total_repayments AS prin_calc,
    lr.prin_current
FROM loan_accounts AS la
    LEFT JOIN (
        SELECT
            account_id,
            COUNT(*) AS total_repayments,
            MEDIAN(principal_installment) AS prin_current
        FROM loan_repayments
        GROUP BY account_id
    ) AS lr USING(account_id)
WHERE la.product_description LIKE '%Fixed Principal%'
ORDER BY
    la.product_description,
    la.product,
    la.account_id
;


/* Loan Repayments */
SELECT
    la.loan_amount,
--     la.loan_amount / COUNT(*) OVER(PARTITION BY la.account_id) AS calc_prin,
--     la.total_term,
    la.total_rate,
    lr.repayment_number,
    lr.repayment_date,
    lr.total_installment,
    lr.principal_installment,
    lr.interest_installment
FROM loan_accounts AS la
    LEFT JOIN loan_repayments AS lr USING(account_id)
WHERE la.account_id = 'AL202498991'
ORDER BY
    la.account_id,
    lr.repayment_number
;


/* Generated Example */
WITH
    cte_raw_data AS (
        SELECT
            2351923.14 AS loan_amount,
            4 AS total_term,
            'quarterly' AS term_type,
            6.3 AS total_rate,
            33750 AS principal_repayment,
            'before' AS before_or_after  /* Whether or not the interest is applied before or after the repayment */
    ),
    cte_repayments AS (
        SELECT
            loan_amount,
            total_term,
            total_rate,
            before_or_after,
            principal_repayment,

            (total_rate / 100.0) / CASE term_type
                WHEN 'yearly'    THEN 1
                WHEN 'quarterly' THEN 4
                WHEN 'monthly'   THEN 12
            END AS periodic_rate,
--             CASE before_or_after
--                 WHEN 'before' THEN 0.01448085
--                 WHEN 'after'  THEN 0.013758505
--             END AS interest_paid_scale,
            CASE before_or_after
                WHEN 'before' THEN total_rate / (100 * 4)
                WHEN 'after'  THEN total_rate / (100 * 4)
            END AS interest_paid_scale,

            0 AS repayment_number,
            0 AS interest_applied,
            0 AS princial_paid,
            0 AS interest_paid,

            loan_amount AS current_balance
        FROM cte_raw_data
    UNION ALL
        SELECT
            loan_amount,
            total_term,
            total_rate,
            before_or_after,
            principal_repayment,

            periodic_rate,
            interest_paid_scale,

            repayment_number + 1 AS repayment_number,
            current_balance * periodic_rate AS interest_applied,
            -principal_repayment AS princial_paid,
            -current_balance * interest_paid_scale AS interest_paid,

            CASE before_or_after
                WHEN 'before' THEN (0
                    + (current_balance * (1 + periodic_rate))
                    - principal_repayment  /* Principal Paid */
                    - (current_balance * interest_paid_scale)  /* Interest Paid */
                    - IIF((repayment_number + 1) = total_term, loan_amount, 0)  /* Balloon Repayment */
                )
                WHEN 'after' THEN (0
                    + current_balance
                    - principal_repayment  /* Principal Paid */
                    - (current_balance * interest_paid_scale)  /* Interest Paid */
                    - IIF((repayment_number + 1) = total_term, loan_amount, 0)  /* Balloon Repayment */
                ) * (1 + periodic_rate)
            END AS current_balance
        FROM cte_repayments
        WHERE repayment_number < total_term
)

SELECT
    loan_amount,
--     total_term,
--     periodic_rate,
    repayment_number,
    ROUND(interest_applied, 2) AS interest_applied,
    ROUND(princial_paid, 2) AS principal_paid,
    ROUND(interest_paid, 2) AS interest_paid,
    ROUND(current_balance, 2) AS current_balance
FROM cte_repayments
;
