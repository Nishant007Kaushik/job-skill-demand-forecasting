USE job_market;

-- 1. Coverage: how many postings have a skill / industry tag at all?
SELECT
  (SELECT COUNT(*) FROM linkedin_postings) AS total_postings,
  (SELECT COUNT(DISTINCT job_id) FROM linkedin_job_skills) AS with_skill,
  (SELECT COUNT(DISTINCT job_id) FROM linkedin_job_industries) AS with_industry;

-- 2. Top skill categories by number of postings
SELECT s.skill_name, COUNT(DISTINCT js.job_id) AS postings,
       ROUND(100 * COUNT(DISTINCT js.job_id) / (SELECT COUNT(*) FROM linkedin_postings), 1) AS pct_of_all
FROM linkedin_job_skills js
JOIN linkedin_skills s ON s.skill_abr = js.skill_abr
GROUP BY s.skill_name ORDER BY postings DESC;

-- 3. Top 15 industries by number of postings
SELECT i.industry_name, COUNT(DISTINCT ji.job_id) AS postings
FROM linkedin_job_industries ji
JOIN linkedin_industries i ON i.industry_id = ji.industry_id
GROUP BY i.industry_name ORDER BY postings DESC LIMIT 15;

-- 4. Explicit remote share by skill category (blank remote_allowed is not counted as on-site)
SELECT s.skill_name, COUNT(DISTINCT p.job_id) AS postings,
       ROUND(100 * SUM(p.remote_allowed = 1) / COUNT(*), 1) AS pct_remote_allowed
FROM linkedin_postings p
JOIN linkedin_job_skills js ON js.job_id = p.job_id
JOIN linkedin_skills s ON s.skill_abr = js.skill_abr
GROUP BY s.skill_name HAVING postings >= 500
ORDER BY pct_remote_allowed DESC;

-- 5. Average applications per posting by skill category (only postings with an applies count)
SELECT s.skill_name, COUNT(*) AS postings, ROUND(AVG(p.applies), 1) AS avg_applies
FROM linkedin_postings p
JOIN linkedin_job_skills js ON js.job_id = p.job_id
JOIN linkedin_skills s ON s.skill_abr = js.skill_abr
WHERE p.applies IS NOT NULL
GROUP BY s.skill_name HAVING postings >= 300
ORDER BY avg_applies DESC;

-- 6. Skill categories that appear together most often
SELECT s1.skill_name AS skill_a, s2.skill_name AS skill_b, COUNT(*) AS postings_together
FROM linkedin_job_skills a
JOIN linkedin_job_skills b ON a.job_id = b.job_id AND a.skill_abr < b.skill_abr
JOIN linkedin_skills s1 ON s1.skill_abr = a.skill_abr
JOIN linkedin_skills s2 ON s2.skill_abr = b.skill_abr
GROUP BY s1.skill_name, s2.skill_name
ORDER BY postings_together DESC LIMIT 15;