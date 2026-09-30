USE job_market;
SELECT COUNT(*) AS total_rows FROM job_postings;
SELECT MIN(posting_date) AS first_date, MAX(posting_date) AS last_date FROM job_postings;
SELECT COUNT(*) AS swapped_salaries FROM job_postings WHERE salary_min > salary_max;