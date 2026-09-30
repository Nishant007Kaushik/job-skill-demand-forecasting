CREATE DATABASE IF NOT EXISTS job_market;
USE job_market;

DROP TABLE IF EXISTS job_postings;
CREATE TABLE job_postings (
  posting_id INT AUTO_INCREMENT PRIMARY KEY,
  posting_date DATE NOT NULL,
  skill VARCHAR(60),
  job_title VARCHAR(80),
  company VARCHAR(80),
  location VARCHAR(60),
  experience_required VARCHAR(20),
  industry VARCHAR(60),
  work_type VARCHAR(20),
  salary_min INT,
  salary_max INT,
  education_level VARCHAR(30),
  employment_type VARCHAR(30),
  job_description TEXT,
  tech_stack VARCHAR(200),
  application_count INT,
  job_posting_source VARCHAR(40),
  trending_skill_flag TINYINT,
  sector_growth_index DECIMAL(4,2)
);