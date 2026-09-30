USE job_market;

-- Does salary depend on experience?
SELECT experience_required, ROUND(AVG((salary_min+salary_max)/2)) AS avg_mid, COUNT(*) AS n
FROM job_postings GROUP BY experience_required
ORDER BY CAST(SUBSTRING_INDEX(experience_required,' ',1) AS UNSIGNED);

-- Does salary depend on skill?
SELECT skill, ROUND(AVG((salary_min+salary_max)/2)) AS avg_mid
FROM job_postings GROUP BY skill ORDER BY avg_mid DESC;

-- Does the trending flag do anything?
SELECT trending_skill_flag, COUNT(*) AS n, ROUND(AVG(application_count),1) AS avg_apps
FROM job_postings GROUP BY trending_skill_flag;