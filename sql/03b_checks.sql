USE job_market;

-- A. Full-row duplicates (all columns except posting_id)
SELECT COUNT(*) AS full_duplicate_groups FROM (
  SELECT 1 FROM job_postings
  GROUP BY posting_date, skill, job_title, company, location, experience_required,
           industry, work_type, salary_min, salary_max, education_level,
           employment_type, tech_stack, application_count, job_posting_source
  HAVING COUNT(*) > 1
) d;

-- B. What are the 4 work types and 13 experience values?
SELECT work_type, COUNT(*) AS n FROM job_postings GROUP BY work_type ORDER BY n DESC;
SELECT experience_required, COUNT(*) AS n FROM job_postings GROUP BY experience_required ORDER BY n DESC;

-- C. Is skill demand flat or does it vary?
SELECT skill, COUNT(*) AS postings FROM job_postings GROUP BY skill ORDER BY postings DESC;

-- D. Is there any trend over time?
SELECT DATE_FORMAT(posting_date, '%Y-%m') AS month, COUNT(*) AS postings
FROM job_postings GROUP BY month ORDER BY month;