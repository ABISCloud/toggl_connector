DROP TABLE IF EXISTS toggl_history;

CREATE TABLE toggl_history (
    id BIGINT PRIMARY KEY,
    User_name VARCHAR(255),
    Client VARCHAR(255),
    Project VARCHAR(255),
    Description TEXT,
    Billable BOOLEAN,
    Start_date DATE,
    Start_time TIME,
    End_date DATE,
    End_time TIME,
    Duration_ms BIGINT,
    Tags TEXT[]
);