CREATE TABLE cominfo (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255),
    website VARCHAR(255),
    url VARCHAR(255),
    description_short VARCHAR(MAX)
);

CREATE TABLE comstatistics (
    com_id VARCHAR(100) FOREIGN KEY REFERENCES companies(id),
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
