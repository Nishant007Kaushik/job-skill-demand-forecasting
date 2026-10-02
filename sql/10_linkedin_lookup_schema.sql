USE job_market;

DROP TABLE IF EXISTS linkedin_job_skills, linkedin_skills, linkedin_job_industries, linkedin_industries;

CREATE TABLE linkedin_skills (
  skill_abr VARCHAR(20) PRIMARY KEY,
  skill_name VARCHAR(100)
);
CREATE TABLE linkedin_job_skills (
  job_id BIGINT NOT NULL,
  skill_abr VARCHAR(20) NOT NULL,
  INDEX idx_js_job (job_id),
  INDEX idx_js_skill (skill_abr)
);
CREATE TABLE linkedin_industries (
  industry_id INT PRIMARY KEY,
  industry_name VARCHAR(200)
);
CREATE TABLE linkedin_job_industries (
  job_id BIGINT NOT NULL,
  industry_id INT NOT NULL,
  INDEX idx_ji_job (job_id),
  INDEX idx_ji_ind (industry_id)
);