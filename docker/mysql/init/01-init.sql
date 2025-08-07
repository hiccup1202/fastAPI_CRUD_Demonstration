-- MySQL initialization script for Product Management API
-- This script creates the database and user for the application

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS product_management
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Create user if it doesn't exist
CREATE USER IF NOT EXISTS 'product_user'@'%' IDENTIFIED BY 'product_password';

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON product_management.* TO 'product_user'@'%';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;

-- Use the database
USE product_management;

-- Create products table if it doesn't exist
CREATE TABLE IF NOT EXISTS products (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_products_name (name(255)),
    INDEX idx_products_price (price)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert some sample data
INSERT INTO products (name, price) VALUES
('Laptop Computer', 150000),
('Smartphone', 80000),
('Wireless Headphones', 25000),
('Gaming Mouse', 15000),
('Mechanical Keyboard', 20000),
('Monitor 27"', 45000),
('USB-C Cable', 2000),
('Power Bank 10000mAh', 8000),
('Bluetooth Speaker', 12000),
('Webcam HD', 15000)
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    price = VALUES(price),
    updated_at = CURRENT_TIMESTAMP; 