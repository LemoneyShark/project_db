CREATE TABLE area (
    id INT PRIMARY KEY,
    type_name VARCHAR(50)
    
);

INSERT INTO area (id, type_name) VALUES (1, 'worldwide'), (2, 'uk');

CREATE TABLE cominfo (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255),
    website VARCHAR(255),
    url VARCHAR(255),
    description_short VARCHAR(MAX),
    area INT,
    CONSTRAINT fk_type FOREIGN KEY (area) REFERENCES area(id)
);

CREATE TABLE comlogs (
    com_id VARCHAR(100) FOREIGN KEY REFERENCES cominfo(id),
    people_count INT,
    senior_people_count INT,
    emails_count INT,
    personal_emails_count INT,
    phones_count INT,
    addresses_count INT,
    investors_count INT,
    clients_count INT,
    partners_count INT,
    changes_count INT,
    people_changes_count INT,
    contact_changes_count INT
);

CREATE TABLE users (
    userID INT PRIMARY KEY IDENTITY(1,1),
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100)
);
