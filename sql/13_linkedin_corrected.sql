USE job_market;

-- 1. How many tag IDs have no matching posting?
SELECT
  (SELECT COUNT(DISTINCT js.job_id) FROM linkedin_job_skills js
     LEFT JOIN linkedin_postings p ON p.job_id = js.job_id WHERE p.job_id IS NULL) AS skill_ids_not_in_postings,
  (SELECT COUNT(DISTINCT ji.job_id) FROM linkedin_job_industries ji
     LEFT JOIN linkedin_postings p ON p.job_id = ji.job_id WHERE p.job_id IS NULL) AS industry_ids_not_in_postings;

-- 2. True coverage: share of postings that have a tag
SELECT COUNT(*) AS total_postings,
  SUM(EXISTS (SELECT 1 FROM linkedin_job_skills js WHERE js.job_id = p.job_id)) AS with_skill,
  SUM(EXISTS (SELECT 1 FROM linkedin_job_industries ji WHERE ji.job_id = p.job_id)) AS with_industry
FROM linkedin_postings p;

-- 3. Views restricted to postings that exist
CREATE OR REPLACE VIEW v_posting_skills AS
SELECT js.job_id, js.skill_abr, s.skill_name
FROM linkedin_job_skills js
JOIN linkedin_skills s ON s.skill_abr = js.skill_abr
JOIN linkedin_postings p ON p.job_id = js.job_id;

CREATE OR REPLACE VIEW v_posting_industries AS
SELECT ji.job_id, ji.industry_id, i.industry_name
FROM linkedin_job_industries ji
JOIN linkedin_industries i ON i.industry_id = ji.industry_id
JOIN linkedin_postings p ON p.job_id = ji.job_id;

-- 4. Corrected top skill categories
SELECT skill_name, COUNT(DISTINCT job_id) AS postings,
       ROUND(100 * COUNT(DISTINCT job_id) / (SELECT COUNT(*) FROM linkedin_postings), 1) AS pct_of_all
FROM v_posting_skills GROUP BY skill_name ORDER BY postings DESC;

-- 5. Corrected top 15 industries
SELECT industry_name, COUNT(DISTINCT job_id) AS postings
FROM v_posting_industries GROUP BY industry_name ORDER BY postings DESC LIMIT 15;

-- 6. Corrected skill pairs
SELECT a.skill_name AS skill_a, b.skill_name AS skill_b, COUNT(*) AS postings_together
FROM v_posting_skills a
JOIN v_posting_skills b ON a.job_id = b.job_id AND a.skill_abr < b.skill_abr
GROUP BY a.skill_name, b.skill_name
ORDER BY postings_together DESC LIMIT 15;