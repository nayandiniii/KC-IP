create database kc_ip;
use kc_ip;

CREATE TABLE user_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    contact VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    kcid VARCHAR(50) UNIQUE,
    password VARCHAR(100)
);
DROP PROCEDURE IF EXISTS GenerateNextKCID;
DELIMITER //

CREATE PROCEDURE GenerateNextKCID(IN prefix VARCHAR(10), OUT next_kcid VARCHAR(50))
BEGIN
    DECLARE last_id INT;
    DECLARE next_id INT;
    DECLARE next_id_str VARCHAR(50);
    
    -- Get the last entered ID for the given prefix
    SELECT SUBSTRING(kcid, LENGTH(prefix) + 1) INTO last_id
    FROM user_details
    WHERE kcid LIKE CONCAT(prefix, '%')
    ORDER BY CAST(SUBSTRING(kcid, LENGTH(prefix) + 1) AS UNSIGNED) DESC
    LIMIT 1;
    
    -- If no record found, set last_id to 0
    IF last_id IS NULL THEN
        SET last_id = 0;
    END IF;

    -- Increment the ID and format it
    SET next_id = last_id + 1;
    
    -- Construct the next KCID
    SET next_kcid = CONCAT(prefix, LPAD(next_id, 3, '0'));
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER BeforeInsertUserDetails
BEFORE INSERT ON user_details
FOR EACH ROW
BEGIN
    DECLARE next_kcid VARCHAR(10);
    
    -- Extract the prefix from the new record
    DECLARE new_prefix VARCHAR(10);
    SET new_prefix = SUBSTRING(NEW.kcid, 1, 3); -- Adjust the length as needed
    
    -- Generate the next KCID based on the extracted prefix
    CALL GenerateNextKCID(new_prefix, next_kcid);
    
    -- Assign the generated KCID to the new record
    SET NEW.kcid = next_kcid;
END //

DELIMITER ;

DROP TRIGGER IF EXISTS BeforeInsertUserDetails;

DELIMITER //

CREATE TRIGGER BeforeInsertUserDetails
BEFORE INSERT ON user_details
FOR EACH ROW
BEGIN
    DECLARE next_kcid VARCHAR(10);
    
    -- Generate the next KCID based on the prefix
    CALL GenerateNextKCID(NEW.kcid, next_kcid);
    
    -- Assign the generated KCID to the new record
    SET NEW.kcid = next_kcid;
END //

DELIMITER ;


-- invoice table--
CREATE TABLE IF NOT EXISTS invoice_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    lead_source VARCHAR(255) NOT NULL,
    lead_month VARCHAR(255) NOT NULL,
    pre_enrollment_number VARCHAR(255),
    about_customer VARCHAR(255) NOT NULL,
    batch_details VARCHAR(255) NOT NULL,
    pitching_model VARCHAR(255) NOT NULL,
    father_name VARCHAR(255) NOT NULL,
    mother_name VARCHAR(255),
    student_name VARCHAR(255) NOT NULL,
    student_age INT NOT NULL,
    current_address VARCHAR(255) NOT NULL,
    school_name VARCHAR(255) NOT NULL,
    contact_number VARCHAR(15) NOT NULL,
    alternative_number VARCHAR(15),
    email VARCHAR(255) NOT NULL,
    course VARCHAR(255) NOT NULL,
    level VARCHAR(255) NOT NULL,
    class_type VARCHAR(255) NOT NULL,
    total_amount int(255) NOT NULL,
    amount_paid INT(255) NOT NULL,
    payment_mode VARCHAR(255) NOT NULL,
    emi_tenure INT,
    emi_per_month INT(255),
    course_duration VARCHAR(255) NOT NULL,
    sales_consultant_name VARCHAR(255) NOT NULL,
    department VARCHAR(255) NOT NULL,
    complementary_course VARCHAR(255) NOT NULL,
    language VARCHAR(255) NOT NULL,
    demo_done VARCHAR(255) NOT NULL,
    complementary_course_details VARCHAR(255),
    image_location VARCHAR(255)
);

drop table invoice_details;

alter table invoice_details add column image_location VARCHAR(255);
alter table invoice_details add column state VARCHAR(255) NOT NULL;


-- MENTOR DETAILS --
CREATE TABLE mentor_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mentor_name VARCHAR(255) NOT NULL,
    birthdate DATE NOT NULL,
    email VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    state VARCHAR(255) NOT NULL,
    education ENUM('Bachelors', 'Masters', 'Doctoral') NOT NULL,
    highest_qualification VARCHAR(255) NOT NULL,
    certifications VARCHAR(255) NOT NULL,
    course VARCHAR(255) NOT NULL,
    level VARCHAR(255) NOT NULL,
    expected_payment DECIMAL(10, 2) NOT NULL,
    available_slots ENUM('Morning', 'Afternoon', 'Evening') NOT NULL
);


-- LEADS DETAILS --
CREATE TABLE leads_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    representative_name VARCHAR(255) NOT NULL,
    mention_lead VARCHAR(255) NOT NULL,
    contact_no VARCHAR(20) NOT NULL,
    address VARCHAR(255) NOT NULL,
    state VARCHAR(50) NOT NULL,
    type_of_lead VARCHAR(50) NOT NULL,
    additional_remarks VARCHAR(255)
);


CREATE TABLE IF NOT EXISTS feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mentor_name VARCHAR(255) NOT NULL,
    student_id VARCHAR(50) NOT NULL,
    material_used INT NOT NULL,
    teaching_methods INT NOT NULL,
    delivery_of_content INT NOT NULL,
    behavior_with_students INT NOT NULL,
    additional_remarks TEXT
);

CREATE TABLE assignment(
    pdf_location VARCHAR(255)
    );

alter table assignment 
add column kcid VARCHAR(255);


alter table assignment add column mentor_id VARCHAR(255);

INSERT INTO user_details (name, age, contact, email, kcid, password)
VALUES ('Priyal', 21, '9418890974', 'pkc@gmail.com', 'KCS001', 'pass123');
truncate assignment;
truncate invoice_details;
truncate mentor_details;
truncate feedback;
truncate leads_details;


select*from user_details;
select*from invoice_details;
select*from mentor_details;
select*from leads_details;
select*from assignment;
select*from feedback;
delete from user_details where email="nandini.september21@gmail.com";
truncate user_details;