-- DB2 Schema Updates for Loan Deferral Feature
-- Run these commands to add credit score and payment history

-- ============================================
-- Step 1: Add credit_score column to customers table
-- ============================================

ALTER TABLE customers 
ADD COLUMN credit_score INTEGER;

-- Update existing customers with credit scores
UPDATE customers SET credit_score = 742 WHERE customer_id = 1;  -- Alice Martinez
UPDATE customers SET credit_score = 755 WHERE customer_id = 2;  -- Brian Nguyen (good credit)
UPDATE customers SET credit_score = 680 WHERE customer_id = 3;  -- Carla Thompson
UPDATE customers SET credit_score = 810 WHERE customer_id = 4;  -- David Kim
UPDATE customers SET credit_score = 725 WHERE customer_id = 5;  -- Elena Okafor
UPDATE customers SET credit_score = 695 WHERE customer_id = 6;  -- Frank Rossi
UPDATE customers SET credit_score = 770 WHERE customer_id = 7;  -- Grace Patel
UPDATE customers SET credit_score = 650 WHERE customer_id = 8;  -- Henry Williams
UPDATE customers SET credit_score = 788 WHERE customer_id = 9;  -- Isabela Cruz
UPDATE customers SET credit_score = 715 WHERE customer_id = 10; -- James Holloway

-- ============================================
-- Step 2: Create payment_history table
-- ============================================

CREATE TABLE payment_history (
    payment_id INTEGER NOT NULL PRIMARY KEY,
    loan_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    payment_date DATE NOT NULL,
    amount_paid DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    days_late INTEGER DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ============================================
-- Step 3: Insert Brian Nguyen's payment history (45 on-time payments)
-- ============================================

-- 2021 payments (6 months)
INSERT INTO payment_history VALUES (1, 1, 2, '2021-07-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (2, 1, 2, '2021-08-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (3, 1, 2, '2021-09-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (4, 1, 2, '2021-10-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (5, 1, 2, '2021-11-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (6, 1, 2, '2021-12-13', 469.35, 'on_time', 0);

-- 2022 payments (12 months)
INSERT INTO payment_history VALUES (7, 1, 2, '2022-01-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (8, 1, 2, '2022-02-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (9, 1, 2, '2022-03-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (10, 1, 2, '2022-04-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (11, 1, 2, '2022-05-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (12, 1, 2, '2022-06-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (13, 1, 2, '2022-07-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (14, 1, 2, '2022-08-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (15, 1, 2, '2022-09-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (16, 1, 2, '2022-10-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (17, 1, 2, '2022-11-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (18, 1, 2, '2022-12-13', 469.35, 'on_time', 0);

-- 2023 payments (12 months)
INSERT INTO payment_history VALUES (19, 1, 2, '2023-01-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (20, 1, 2, '2023-02-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (21, 1, 2, '2023-03-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (22, 1, 2, '2023-04-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (23, 1, 2, '2023-05-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (24, 1, 2, '2023-06-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (25, 1, 2, '2023-07-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (26, 1, 2, '2023-08-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (27, 1, 2, '2023-09-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (28, 1, 2, '2023-10-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (29, 1, 2, '2023-11-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (30, 1, 2, '2023-12-13', 469.35, 'on_time', 0);

-- 2024 payments (12 months)
INSERT INTO payment_history VALUES (31, 1, 2, '2024-01-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (32, 1, 2, '2024-02-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (33, 1, 2, '2024-03-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (34, 1, 2, '2024-04-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (35, 1, 2, '2024-05-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (36, 1, 2, '2024-06-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (37, 1, 2, '2024-07-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (38, 1, 2, '2024-08-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (39, 1, 2, '2024-09-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (40, 1, 2, '2024-10-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (41, 1, 2, '2024-11-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (42, 1, 2, '2024-12-13', 469.35, 'on_time', 0);

-- 2025 payments (3 months so far)
INSERT INTO payment_history VALUES (43, 1, 2, '2025-01-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (44, 1, 2, '2025-02-13', 469.35, 'on_time', 0);
INSERT INTO payment_history VALUES (45, 1, 2, '2025-03-13', 469.35, 'on_time', 0);

-- ============================================
-- Step 4: Verify the changes
-- ============================================

-- Check credit scores were added
SELECT customer_id, first_name, last_name, email, credit_score 
FROM customers 
ORDER BY customer_id;

-- Check payment history was created
SELECT COUNT(*) as total_payments, 
       SUM(CASE WHEN status = 'on_time' THEN 1 ELSE 0 END) as on_time_payments,
       SUM(CASE WHEN status = 'late' THEN 1 ELSE 0 END) as late_payments
FROM payment_history 
WHERE customer_id = 2;

-- Check Brian's payment history details
SELECT payment_id, payment_date, amount_paid, status, days_late
FROM payment_history
WHERE customer_id = 2
ORDER BY payment_date DESC
LIMIT 10;

-- Made with Bob
