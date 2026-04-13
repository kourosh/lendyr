-- Add Payment Histories for 5 Lendyr Customers
-- This script adds payment records for Carla, Elena, Frank, Henry, and Isabela
-- Payment IDs start from 76 (Brian uses 1-75)

-- ============================================
-- 1. Carla Thompson (Customer ID: 3, Loan ID: 2)
-- Mortgage: $5,363.33/month
-- 28 payments: 26 on-time, 2 late
-- Period: January 2024 - April 2026
-- ============================================

-- 2024 payments (12 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES (76, 2, 3, '2024-01-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (77, 2, 3, '2024-02-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (78, 2, 3, '2024-03-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (79, 2, 3, '2024-04-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (80, 2, 3, '2024-05-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (81, 2, 3, '2024-06-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (82, 2, 3, '2024-07-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (83, 2, 3, '2024-08-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (84, 2, 3, '2024-09-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (85, 2, 3, '2024-10-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (86, 2, 3, '2024-11-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (87, 2, 3, '2024-12-15', 5363.33, 'on_time', 0);

-- 2025 payments (12 months, 2 late: March and September)
INSERT INTO "LENDYR-DEMO".payment_history VALUES (88, 2, 3, '2025-01-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (89, 2, 3, '2025-02-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (90, 2, 3, '2025-03-20', 5363.33, 'late', 5);  -- 5 days late
INSERT INTO "LENDYR-DEMO".payment_history VALUES (91, 2, 3, '2025-04-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (92, 2, 3, '2025-05-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (93, 2, 3, '2025-06-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (94, 2, 3, '2025-07-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (95, 2, 3, '2025-08-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (96, 2, 3, '2025-09-27', 5363.33, 'late', 12);  -- 12 days late
INSERT INTO "LENDYR-DEMO".payment_history VALUES (97, 2, 3, '2025-10-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (98, 2, 3, '2025-11-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (99, 2, 3, '2025-12-15', 5363.33, 'on_time', 0);

-- 2026 payments (4 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES (100, 2, 3, '2026-01-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (101, 2, 3, '2026-02-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (102, 2, 3, '2026-03-15', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (103, 2, 3, '2026-04-15', 5363.33, 'on_time', 0);

-- ============================================
-- 2. Elena Okafor (Customer ID: 5, Loan ID: 3)
-- Personal Loan: $252.60/month
-- 24 payments: all on-time
-- Period: May 2024 - April 2026
-- ============================================

-- 2024 payments (8 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES (104, 3, 5, '2024-05-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (105, 3, 5, '2024-06-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (106, 3, 5, '2024-07-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (107, 3, 5, '2024-08-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (108, 3, 5, '2024-09-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (109, 3, 5, '2024-10-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (110, 3, 5, '2024-11-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (111, 3, 5, '2024-12-16', 252.60, 'on_time', 0);

-- 2025 payments (12 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES (112, 3, 5, '2025-01-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (113, 3, 5, '2025-02-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (114, 3, 5, '2025-03-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (115, 3, 5, '2025-04-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (116, 3, 5, '2025-05-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (117, 3, 5, '2025-06-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (118, 3, 5, '2025-07-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (119, 3, 5, '2025-08-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (120, 3, 5, '2025-09-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (121, 3, 5, '2025-10-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (122, 3, 5, '2025-11-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (123, 3, 5, '2025-12-16', 252.60, 'on_time', 0);

-- 2026 payments (4 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES (124, 3, 5, '2026-01-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (125, 3, 5, '2026-02-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (126, 3, 5, '2026-03-16', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (127, 3, 5, '2026-04-16', 252.60, 'on_time', 0);

-- ============================================
-- 3. Frank Rossi (Customer ID: 6, Loan ID: 4)
-- Mortgage: $5,363.33/month
-- 18 payments: 17 on-time, 1 late
-- Period: November 2024 - April 2026
-- ============================================

-- 2024 payments (2 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES (128, 4, 6, '2024-11-17', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (129, 4, 6, '2024-12-17', 5363.33, 'on_time', 0);

-- 2025 payments (12 months, 1 late in February)
INSERT INTO "LENDYR-DEMO".payment_history VALUES (130, 4, 6, '2025-01-17', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (131, 4, 6, '2025-02-25', 5363.33, 'late', 8);  -- 8 days late
INSERT INTO "LENDYR-DEMO".payment_history VALUES (132, 4, 6, '2025-03-17', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (133, 4, 6, '2025-04-17', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (134, 4, 6, '2025-05-17', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (135, 4, 6, '2025-06-17', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (136, 4, 6, '2025-07-17', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (137, 4, 6, '2025-08-17', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (138, 4, 6, '2025-09-17', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (139, 4, 6, '2025-10-17', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (140, 4, 6, '2025-11-17', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (141, 4, 6, '2025-12-17', 5363.33, 'on_time', 0);

-- 2026 payments (4 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES (142, 4, 6, '2026-01-17', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (143, 4, 6, '2026-02-17', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (144, 4, 6, '2026-03-17', 5363.33, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (145, 4, 6, '2026-04-17', 5363.33, 'on_time', 0);

-- ============================================
-- 4. Henry Williams (Customer ID: 8, Loan ID: 5)
-- Auto Loan: $469.35/month
-- 12 payments: 10 on-time, 2 late
-- Period: May 2025 - April 2026
-- ============================================

-- 2025 payments (8 months, 2 late: August and December)
INSERT INTO "LENDYR-DEMO".payment_history VALUES (146, 5, 8, '2025-05-18', 469.35, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (147, 5, 8, '2025-06-18', 469.35, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (148, 5, 8, '2025-07-18', 469.35, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (149, 5, 8, '2025-08-02', 469.35, 'late', 15);  -- 15 days late
INSERT INTO "LENDYR-DEMO".payment_history VALUES (150, 5, 8, '2025-09-18', 469.35, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (151, 5, 8, '2025-10-18', 469.35, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (152, 5, 8, '2025-11-18', 469.35, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (153, 5, 8, '2026-01-09', 469.35, 'late', 22);  -- 22 days late

-- 2026 payments (4 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES (154, 5, 8, '2026-01-18', 469.35, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (155, 5, 8, '2026-02-18', 469.35, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (156, 5, 8, '2026-03-18', 469.35, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (157, 5, 8, '2026-04-18', 469.35, 'on_time', 0);

-- ============================================
-- 5. Isabela Cruz (Customer ID: 9, Loan ID: 6)
-- Personal Loan: $252.60/month
-- 30 payments: all on-time
-- Period: November 2023 - April 2026
-- ============================================

-- 2023 payments (2 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES (158, 6, 9, '2023-11-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (159, 6, 9, '2023-12-19', 252.60, 'on_time', 0);

-- 2024 payments (12 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES (160, 6, 9, '2024-01-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (161, 6, 9, '2024-02-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (162, 6, 9, '2024-03-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (163, 6, 9, '2024-04-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (164, 6, 9, '2024-05-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (165, 6, 9, '2024-06-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (166, 6, 9, '2024-07-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (167, 6, 9, '2024-08-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (168, 6, 9, '2024-09-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (169, 6, 9, '2024-10-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (170, 6, 9, '2024-11-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (171, 6, 9, '2024-12-19', 252.60, 'on_time', 0);

-- 2025 payments (12 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES (172, 6, 9, '2025-01-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (173, 6, 9, '2025-02-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (174, 6, 9, '2025-03-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (175, 6, 9, '2025-04-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (176, 6, 9, '2025-05-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (177, 6, 9, '2025-06-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (178, 6, 9, '2025-07-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (179, 6, 9, '2025-08-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (180, 6, 9, '2025-09-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (181, 6, 9, '2025-10-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (182, 6, 9, '2025-11-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (183, 6, 9, '2025-12-19', 252.60, 'on_time', 0);

-- 2026 payments (4 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES (184, 6, 9, '2026-01-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (185, 6, 9, '2026-02-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (186, 6, 9, '2026-03-19', 252.60, 'on_time', 0);
INSERT INTO "LENDYR-DEMO".payment_history VALUES (187, 6, 9, '2026-04-19', 252.60, 'on_time', 0);

-- ============================================
-- Verification Queries
-- ============================================

-- Count total payments by customer
SELECT c.customer_id, c.first_name, c.last_name,
       COUNT(ph.payment_id) as total_payments,
       SUM(CASE WHEN ph.status = 'on_time' THEN 1 ELSE 0 END) as on_time,
       SUM(CASE WHEN ph.status = 'late' THEN 1 ELSE 0 END) as late
FROM "LENDYR-DEMO".customers c
LEFT JOIN "LENDYR-DEMO".payment_history ph ON c.customer_id = ph.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_payments DESC;

-- Total payment records in database
SELECT COUNT(*) as total_payment_records FROM "LENDYR-DEMO".payment_history;

-- Made with Bob
