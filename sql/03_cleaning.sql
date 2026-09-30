USE job_market;

-- 1. Exact duplicate postings (same date, skill, title, company, location)
SELECT posting_date, skill, job_title, company, location, COUNT(*) AS copies
FROM job_postings
GROUP BY posting_date, skill, job_title, company, location
HAVING COUNT(*) > 1
ORDER BY copies DESC
LIMIT 20;

-- 2. Text consistency: distinct values per category column
SELECT 'skill' AS col, COUNT(DISTINCT skill) AS distinct_values FROM job_postings
UNION ALL SELECT 'job_title', COUNT(DISTINCT job_title) FROM job_postings
UNION ALL SELECT 'location', COUNT(DISTINCT location) FROM job_postings
UNION ALL SELECT 'industry', COUNT(DISTINCT industry) FROM job_postings
UNION ALL SELECT 'work_type', COUNT(DISTINCT work_type) FROM job_postings
UNION ALL SELECT 'experience_required', COUNT(DISTINCT experience_required) FROM job_postings;

-- 3. Spelling or case variants (same value when lowercased and trimmed, different when raw)
SELECT LOWER(TRIM(skill)) AS skill_clean, COUNT(DISTINCT skill) AS variants
FROM job_postings
GROUP BY LOWER(TRIM(skill))
HAVING COUNT(DISTINCT skill) > 1;

-- 4. Missing values per column
SELECT
  SUM(skill IS NULL OR skill = '')                 AS missing_skill,
  SUM(job_title IS NULL OR job_title = '')         AS missing_title,
  SUM(company IS NULL OR company = '')             AS missing_company,
  SUM(salary_min IS NULL)                          AS missing_salary_min,
  SUM(salary_max IS NULL)                          AS missing_salary_max,
  SUM(application_count IS NULL)                   AS missing_applications
FROM job_postings;

-- 5. Salary outliers and unrealistic pay
SELECT MIN(salary_min) AS lowest_min, MAX(salary_max) AS highest_max,
       ROUND(AVG((salary_min + salary_max) / 2)) AS avg_mid
FROM job_postings;

SELECT job_title, experience_required, salary_min, salary_max
FROM job_postings
WHERE job_title LIKE '%Intern%' AND salary_max > 1500000
LIMIT 20;

-- 6. Title and skill mismatch, e.g. a JavaScript posting for an AI researcher
SELECT skill, job_title, COUNT(*) AS postings
FROM job_postings
GROUP BY skill, job_title
ORDER BY postings DESC
LIMIT 25;