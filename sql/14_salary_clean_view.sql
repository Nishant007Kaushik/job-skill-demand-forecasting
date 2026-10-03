USE job_market;

CREATE OR REPLACE VIEW v_salary_clean AS
SELECT * FROM (
  SELECT job_id, title, formatted_work_type, formatted_experience_level, location, pay_period,
         CASE WHEN pay_period = 'HOURLY' AND max_salary >= 1000
              THEN (min_salary + max_salary) / 2
              ELSE normalized_salary END AS annual_pay_usd
  FROM linkedin_postings
  WHERE currency = 'USD' AND normalized_salary IS NOT NULL
) t
WHERE annual_pay_usd BETWEEN 15000 AND 1000000;

-- 1. How many salaries survive the cleaning?
SELECT (SELECT COUNT(*) FROM linkedin_postings WHERE currency = 'USD' AND normalized_salary IS NOT NULL) AS usd_with_pay,
       COUNT(*) AS kept_after_cleaning FROM v_salary_clean;

-- 2. Overall median annual pay
SELECT ROUND(AVG(annual_pay_usd)) AS median_annual_pay_usd, MAX(cnt) AS n FROM (
  SELECT annual_pay_usd,
         ROW_NUMBER() OVER (ORDER BY annual_pay_usd) AS rn,
         COUNT(*) OVER () AS cnt
  FROM v_salary_clean) x
WHERE rn IN (FLOOR((cnt + 1) / 2), CEIL((cnt + 1) / 2));

-- 3. Median annual pay by experience level
SELECT formatted_experience_level, MAX(cnt) AS n, ROUND(AVG(annual_pay_usd)) AS median_pay_usd FROM (
  SELECT formatted_experience_level, annual_pay_usd,
         ROW_NUMBER() OVER (PARTITION BY formatted_experience_level ORDER BY annual_pay_usd) AS rn,
         COUNT(*) OVER (PARTITION BY formatted_experience_level) AS cnt
  FROM v_salary_clean) x
WHERE rn IN (FLOOR((cnt + 1) / 2), CEIL((cnt + 1) / 2))
GROUP BY formatted_experience_level ORDER BY median_pay_usd DESC;

-- 4. Median annual pay by work type
SELECT formatted_work_type, MAX(cnt) AS n, ROUND(AVG(annual_pay_usd)) AS median_pay_usd FROM (
  SELECT formatted_work_type, annual_pay_usd,
         ROW_NUMBER() OVER (PARTITION BY formatted_work_type ORDER BY annual_pay_usd) AS rn,
         COUNT(*) OVER (PARTITION BY formatted_work_type) AS cnt
  FROM v_salary_clean) x
WHERE rn IN (FLOOR((cnt + 1) / 2), CEIL((cnt + 1) / 2))
GROUP BY formatted_work_type ORDER BY median_pay_usd DESC;

-- 5. Median annual pay by skill category (a posting counts once per category it carries)
SELECT skill_name, MAX(cnt) AS n, ROUND(AVG(annual_pay_usd)) AS median_pay_usd FROM (
  SELECT ps.skill_name, c.annual_pay_usd,
         ROW_NUMBER() OVER (PARTITION BY ps.skill_name ORDER BY c.annual_pay_usd) AS rn,
         COUNT(*) OVER (PARTITION BY ps.skill_name) AS cnt
  FROM v_salary_clean c JOIN v_posting_skills ps ON ps.job_id = c.job_id) x
WHERE rn IN (FLOOR((cnt + 1) / 2), CEIL((cnt + 1) / 2))
GROUP BY skill_name HAVING n >= 200 ORDER BY median_pay_usd DESC;