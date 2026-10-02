USE job_market;

SELECT
  SUM(normalized_salary = 0)                       AS zero_pay,
  SUM(normalized_salary > 0 AND normalized_salary < 15000)  AS under_15k,
  SUM(normalized_salary BETWEEN 15000 AND 1000000) AS plausible,
  SUM(normalized_salary > 1000000)                 AS over_1m
FROM linkedin_postings WHERE currency = 'USD';

SELECT pay_period, COUNT(*) AS n, ROUND(MAX(normalized_salary)) AS max_pay
FROM linkedin_postings
WHERE currency = 'USD' AND normalized_salary > 1000000
GROUP BY pay_period;

SELECT job_id, title, pay_period, min_salary, max_salary, normalized_salary
FROM linkedin_postings
WHERE currency = 'USD' AND normalized_salary > 1000000
ORDER BY normalized_salary DESC LIMIT 10;