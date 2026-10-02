USE job_market;

-- A. What is in the under-15k bucket?
SELECT pay_period, COUNT(*) AS n,
       ROUND(MIN(normalized_salary)) AS min_pay, ROUND(MAX(normalized_salary)) AS max_pay
FROM linkedin_postings
WHERE currency = 'USD' AND normalized_salary > 0 AND normalized_salary < 15000
GROUP BY pay_period;

-- B. A random sample of those rows
SELECT job_id, title, formatted_work_type, pay_period, min_salary, max_salary, normalized_salary
FROM linkedin_postings
WHERE currency = 'USD' AND normalized_salary > 0 AND normalized_salary < 15000
ORDER BY RAND() LIMIT 15;

-- C. How many HOURLY rows have yearly-sized figures?
SELECT COUNT(*) AS hourly_looks_yearly
FROM linkedin_postings
WHERE currency = 'USD' AND pay_period = 'HOURLY' AND max_salary >= 1000;