-- create_schema.sql
-- تنظیمات برای فعال کردن Foreign Keys در SQLite
PRAGMA foreign_keys = ON;

-- حذف جداول در صورت وجود (برای شروع تمیز)
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Seller;
DROP TABLE IF EXISTS Manager;


-- 1. جدول Manager (مدیران)
CREATE TABLE Manager (
    manager_id INTEGER PRIMARY KEY,
    manager_name TEXT NOT NULL
);

-- 2. جدول Customer (خریداران)
CREATE TABLE Customer (
    cust_id INTEGER PRIMARY KEY,
    cust_name TEXT NOT NULL,
    city TEXT,
    manager_id INTEGER, -- کلید خارجی به Manager
    
    FOREIGN KEY (manager_id) 
        REFERENCES Manager(manager_id) 
        -- اگر یک مدیر حذف شود، manager_id در مشتریان او NULL می‌شود (مشتری بدون مدیر می‌ماند)
        ON DELETE SET NULL 
);

-- 3. جدول Seller (فروشندگان)
CREATE TABLE Seller (
    seller_id INTEGER PRIMARY KEY,
    seller_name TEXT NOT NULL,
    city TEXT
);

-- 4. جدول Orders (سفارشات)
CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY,
    cust_id INTEGER NOT NULL, -- کلید خارجی به Customer
    seller_id INTEGER NOT NULL, -- کلید خارجی به Seller
    amount REAL NOT NULL,
    order_date TEXT NOT NULL,
    
    FOREIGN KEY (cust_id) 
        REFERENCES Customer(cust_id) 
        -- اگر خریدار حذف شود، سفارشات او نیز حذف می‌شوند (CASCADE)
        ON DELETE CASCADE, 
    
    FOREIGN KEY (seller_id) 
        REFERENCES Seller(seller_id)
        -- اگر فروشنده حذف شود، سفارشات مرتبط نیز حذف می‌شوند (CASCADE)
        ON DELETE CASCADE
);

-- درج داده‌های نمونه (اختیاری، اما برای تست کوئری‌ها مفید است)
INSERT INTO Manager (manager_id, manager_name) VALUES (101, 'مدیر الف');
INSERT INTO Manager (manager_id, manager_name) VALUES (102, 'مدیر ب');

INSERT INTO Customer (cust_id, cust_name, city, manager_id) VALUES (201, 'خریدار 1', 'تهران', 101);
INSERT INTO Customer (cust_id, cust_name, city, manager_id) VALUES (202, 'خریدار 2', 'تبریز', 102);
INSERT INTO Customer (cust_id, cust_name, city, manager_id) VALUES (203, 'خریدار 3', 'تهران', 101); -- خریدار بدون سفارش برای تست
INSERT INTO Customer (cust_id, cust_name, city, manager_id) VALUES (204, 'خریدار 4', 'اصفهان', NULL); -- خریدار بدون مدیر برای تست

INSERT INTO Seller (seller_id, seller_name, city) VALUES (301, 'فروشنده 1', 'تهران');
INSERT INTO Seller (seller_id, seller_name, city) VALUES (302, 'فروشنده 2', 'مشهد');

INSERT INTO Orders (order_id, cust_id, seller_id, amount, order_date) VALUES (401, 201, 301, 1500.00, '2025-11-01');
INSERT INTO Orders (order_id, cust_id, seller_id, amount, order_date) VALUES (402, 202, 302, 250.50, '2025-11-02');
INSERT INTO Orders (order_id, cust_id, seller_id, amount, order_date) VALUES (403, 201, 302, 800.00, '2025-11-03');
INSERT INTO Orders (order_id, cust_id, seller_id, amount, order_date) VALUES (404, 204, 301, 400.00, '2025-11-04');
