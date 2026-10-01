USE job_market;

DROP TABLE IF EXISTS linkedin_postings;
CREATE TABLE linkedin_postings (
  job_id BIGINT NOT NULL,
  company_name VARCHAR(500),
  title VARCHAR(500),
  location VARCHAR(500),
  company_id BIGINT,
  formatted_work_type VARCHAR(50),
  work_type VARCHAR(50),
  formatted_experience_level VARCHAR(50),
  remote_allowed TINYINT,
  sponsored TINYINT,
  application_type VARCHAR(50),
  posting_domain VARCHAR(500),
  pay_period VARCHAR(30),
  currency VARCHAR(10),
  compensation_type VARCHAR(50),
  min_salary DOUBLE,
  med_salary DOUBLE,
  max_salary DOUBLE,
  normalized_salary DOUBLE,
  views INT,
  applies INT,
  listed_time DATETIME,
  original_listed_time DATETIME,
  closed_time DATETIME,
  expiry DATETIME,
  skills_desc TEXT,
  INDEX idx_job_id (job_id),
  INDEX idx_title (title(100)),
  INDEX idx_listed (listed_time)
);