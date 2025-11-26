-- Create database
CREATE DATABASE IF NOT EXISTS blog_website;

-- Use the database
USE blog_website;

-- Create stories table
CREATE TABLE IF NOT EXISTS stories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    author_name VARCHAR(255) NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    content TEXT NOT NULL,
    photo_url VARCHAR(500) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create admin users table
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default admin credentials
-- Username: admin
-- Password: admin123
-- IMPORTANT: Change these credentials after first login!
INSERT INTO admin_users (username, password) 
VALUES ('sidhu', 'sidhu123')
ON DUPLICATE KEY UPDATE username=username;

-- Display success message
SELECT 'Database setup completed successfully!' AS message;