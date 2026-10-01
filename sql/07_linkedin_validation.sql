USE job_market;
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT job_id) AS distinct_ids FROM linkedin_postings;
SELECT MIN(listed_time) AS first_listed, MAX(listed_time) AS last_listed FROM linkedin_postings;
SELECT COUNT(*) AS with_salary, ROUND(100*COUNT(*)/(SELECT COUNT(*) FROM linkedin_postings),1) AS pct
FROM linkedin_postings WHERE normalized_salary IS NOT NULL;
SELECT currency, COUNT(*) AS n FROM linkedin_postings GROUP BY currency ORDER BY n DESC;
SELECT formatted_work_type, COUNT(*) AS n FROM linkedin_postings GROUP BY formatted_work_type ORDER BY n DESC;