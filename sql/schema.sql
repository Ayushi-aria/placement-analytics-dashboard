CREATE DATABASE placement_db;
USE placement_db;

CREATE TABLE students (
    student_id INT PRIMARY KEY,
    branch VARCHAR(50),
    cgpa DECIMAL(3,2),
    batch_year INT
);

CREATE TABLE companies (
    company_id INT PRIMARY KEY,
    company_name VARCHAR(100),
    sector VARCHAR(50),
    ctc_lpa DECIMAL(5,2)
);

CREATE TABLE applications (
    application_id INT PRIMARY KEY,
    student_id INT,
    company_id INT,
    stage_reached VARCHAR(20),  -- Applied / OA / Interview / Offer
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE offers (
    offer_id INT PRIMARY KEY,
    student_id INT,
    company_id INT,
    ctc_lpa DECIMAL(5,2),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);
