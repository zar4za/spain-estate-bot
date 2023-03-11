CREATE TABLE articles
(
    id INT PRIMARY KEY,
    title VARCHAR(64),
    specs VARCHAR(256),
    description VARCHAR(512)
)
CREATE TABLE users
(
    userid integer NOT NULL,
    trial boolean,
    valid_until timestamp without time zone,
    CONSTRAINT users_pkey PRIMARY KEY (userid)
)