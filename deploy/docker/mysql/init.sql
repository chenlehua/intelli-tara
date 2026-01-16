-- MySQL initialization script for Intelli-TARA

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS intelli_tara CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use the database
USE intelli_tara;

-- Grant privileges
GRANT ALL PRIVILEGES ON intelli_tara.* TO 'intelli_tara'@'%';
FLUSH PRIVILEGES;
