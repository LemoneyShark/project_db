CREATE TABLE cominfo (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255),
    website VARCHAR(255),
    url VARCHAR(255),
    description_short VARCHAR(MAX),
    type INT
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

CREATE TABLE type (
    id INT PRIMARY KEY,
    type_name VARCHAR(50)
);

INSERT INTO type (id, type_name) VALUES (1, 'worldwide'), (2, 'uk');


ALTER TABLE cominfo
ADD CONSTRAINT fk_type FOREIGN KEY (type) REFERENCES type(id);
