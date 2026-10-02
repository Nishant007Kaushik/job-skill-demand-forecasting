USE job_market;

-- 1. Sanity check on normalized salary (USD only): should be annual pay
SELECT MIN(normalized_salary) AS min_pay, MAX(normalized_salary) AS max_pay,
       ROUND(AVG(normalized_salary)) AS avg_pay
FROM linkedin_postings WHERE currency = 'USD';

-- 2. Top 15 job titles by posting count
SELECT title, COUNT(*) AS postings
FROM linkedin_postings GROUP BY title ORDER BY postings DESC LIMIT 15;

-- 3. Top 15 locations (is this mostly US?)
SELECT location, COUNT(*) AS postings
FROM linkedin_postings GROUP BY location ORDER BY postings DESC LIMIT 15;

-- 4. Experience level mix
SELECT formatted_experience_level, COUNT(*) AS postings
FROM linkedin_postings GROUP BY formatted_experience_level ORDER BY postings DESC;

-- 5. Median-ish pay by work type (average, USD only, salary present)
SELECT formatted_work_type, COUNT(*) AS postings_with_pay,
       ROUND(AVG(normalized_salary)) AS avg_annual_pay
FROM linkedin_postings
WHERE currency = 'USD' AND normalized_salary IS NOT NULL
GROUP BY formatted_work_type ORDER BY avg_annual_pay DESC;

-- 6. Remote-allowed share
SELECT remote_allowed, COUNT(*) AS postings,
       ROUND(100 * COUNT(*) / (SELECT COUNT(*) FROM linkedin_postings), 1) AS pct
FROM linkedin_postings GROUP BY remote_allowed;

-- 7. Applications per posting by experience level
SELECT formatted_experience_level, ROUND(AVG(applies), 1) AS avg_applies, COUNT(*) AS postings
FROM linkedin_postings WHERE applies IS NOT NULL
GROUP BY formatted_experience_level ORDER BY avg_applies DESC;