CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL, 
  	age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  	tags VARCHAR(1000) NOT NULL                      -- Change VARCHAR to TEXT
);
INSERT INTO Users (username, email, password, age, tags)
VALUES
('john_doe', 'john@example.com', 'hashed_password1', 30, 'developer, tech'),
('jane_smith', 'jane@example.com', 'hashed_password2', 25, 'designer, art');

SELECT email, age, tags
FROM Users; 
