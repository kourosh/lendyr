-- Add Payment Histories for 5 Lendyr Customers
-- Updated to match actual table structure
-- Columns: PAYMENT_ID, CUSTOMER_ID, PAYMENT_DATE, PAYMENT_AMOUNT, AUTO_PAY_USED, WAS_LATE, DAYS_LATE, NOTE

-- ============================================
-- 1. Carla Thompson (Customer ID: 3, Loan ID: 2)
-- Mortgage: $5,363.33/month
-- 28 payments: 26 on-time, 2 late
-- Period: January 2024 - April 2026
-- ============================================

-- 2024 payments (12 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('76', '3', '2024-01-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('77', '3', '2024-02-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('78', '3', '2024-03-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('79', '3', '2024-04-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('80', '3', '2024-05-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('81', '3', '2024-06-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('82', '3', '2024-07-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('83', '3', '2024-08-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('84', '3', '2024-09-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('85', '3', '2024-10-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('86', '3', '2024-11-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('87', '3', '2024-12-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');

-- 2025 payments (12 months, 2 late: March and September)
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('88', '3', '2025-01-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('89', '3', '2025-02-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('90', '3', '2025-03-20', 5363.33, 0, 1, 5, 'Late payment - 5 days');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('91', '3', '2025-04-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('92', '3', '2025-05-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('93', '3', '2025-06-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('94', '3', '2025-07-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('95', '3', '2025-08-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('96', '3', '2025-09-27', 5363.33, 0, 1, 12, 'Late payment - 12 days');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('97', '3', '2025-10-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('98', '3', '2025-11-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('99', '3', '2025-12-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');

-- 2026 payments (4 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('100', '3', '2026-01-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('101', '3', '2026-02-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('102', '3', '2026-03-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('103', '3', '2026-04-15', 5363.33, 0, 0, 0, 'Monthly mortgage payment');

-- ============================================
-- 2. Elena Okafor (Customer ID: 5, Loan ID: 3)
-- Personal Loan: $252.60/month
-- 24 payments: all on-time
-- Period: May 2024 - April 2026
-- ============================================

-- 2024 payments (8 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('104', '5', '2024-05-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('105', '5', '2024-06-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('106', '5', '2024-07-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('107', '5', '2024-08-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('108', '5', '2024-09-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('109', '5', '2024-10-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('110', '5', '2024-11-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('111', '5', '2024-12-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');

-- 2025 payments (12 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('112', '5', '2025-01-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('113', '5', '2025-02-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('114', '5', '2025-03-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('115', '5', '2025-04-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('116', '5', '2025-05-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('117', '5', '2025-06-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('118', '5', '2025-07-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('119', '5', '2025-08-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('120', '5', '2025-09-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('121', '5', '2025-10-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('122', '5', '2025-11-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('123', '5', '2025-12-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');

-- 2026 payments (4 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('124', '5', '2026-01-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('125', '5', '2026-02-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('126', '5', '2026-03-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('127', '5', '2026-04-16', 252.60, 0, 0, 0, 'Monthly personal loan payment');

-- ============================================
-- 3. Frank Rossi (Customer ID: 6, Loan ID: 4)
-- Mortgage: $5,363.33/month
-- 18 payments: 17 on-time, 1 late
-- Period: November 2024 - April 2026
-- ============================================

-- 2024 payments (2 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('128', '6', '2024-11-17', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('129', '6', '2024-12-17', 5363.33, 0, 0, 0, 'Monthly mortgage payment');

-- 2025 payments (12 months, 1 late in February)
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('130', '6', '2025-01-17', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('131', '6', '2025-02-25', 5363.33, 0, 1, 8, 'Late payment - 8 days');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('132', '6', '2025-03-17', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('133', '6', '2025-04-17', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('134', '6', '2025-05-17', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('135', '6', '2025-06-17', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('136', '6', '2025-07-17', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('137', '6', '2025-08-17', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('138', '6', '2025-09-17', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('139', '6', '2025-10-17', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('140', '6', '2025-11-17', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('141', '6', '2025-12-17', 5363.33, 0, 0, 0, 'Monthly mortgage payment');

-- 2026 payments (4 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('142', '6', '2026-01-17', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('143', '6', '2026-02-17', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('144', '6', '2026-03-17', 5363.33, 0, 0, 0, 'Monthly mortgage payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('145', '6', '2026-04-17', 5363.33, 0, 0, 0, 'Monthly mortgage payment');

-- ============================================
-- 4. Henry Williams (Customer ID: 8, Loan ID: 5)
-- Auto Loan: $469.35/month
-- 12 payments: 10 on-time, 2 late
-- Period: May 2025 - April 2026
-- ============================================

-- 2025 payments (8 months, 2 late: August and December)
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('146', '8', '2025-05-18', 469.35, 0, 0, 0, 'Monthly auto loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('147', '8', '2025-06-18', 469.35, 0, 0, 0, 'Monthly auto loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('148', '8', '2025-07-18', 469.35, 0, 0, 0, 'Monthly auto loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('149', '8', '2025-08-02', 469.35, 0, 1, 15, 'Late payment - 15 days');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('150', '8', '2025-09-18', 469.35, 0, 0, 0, 'Monthly auto loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('151', '8', '2025-10-18', 469.35, 0, 0, 0, 'Monthly auto loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('152', '8', '2025-11-18', 469.35, 0, 0, 0, 'Monthly auto loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('153', '8', '2026-01-09', 469.35, 0, 1, 22, 'Late payment - 22 days');

-- 2026 payments (4 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('154', '8', '2026-01-18', 469.35, 0, 0, 0, 'Monthly auto loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('155', '8', '2026-02-18', 469.35, 0, 0, 0, 'Monthly auto loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('156', '8', '2026-03-18', 469.35, 0, 0, 0, 'Monthly auto loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('157', '8', '2026-04-18', 469.35, 0, 0, 0, 'Monthly auto loan payment');

-- ============================================
-- 5. Isabela Cruz (Customer ID: 9, Loan ID: 6)
-- Personal Loan: $252.60/month
-- 30 payments: all on-time
-- Period: November 2023 - April 2026
-- ============================================

-- 2023 payments (2 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('158', '9', '2023-11-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('159', '9', '2023-12-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');

-- 2024 payments (12 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('160', '9', '2024-01-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('161', '9', '2024-02-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('162', '9', '2024-03-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('163', '9', '2024-04-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('164', '9', '2024-05-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('165', '9', '2024-06-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('166', '9', '2024-07-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('167', '9', '2024-08-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('168', '9', '2024-09-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('169', '9', '2024-10-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('170', '9', '2024-11-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('171', '9', '2024-12-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');

-- 2025 payments (12 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('172', '9', '2025-01-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('173', '9', '2025-02-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('174', '9', '2025-03-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('175', '9', '2025-04-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('176', '9', '2025-05-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('177', '9', '2025-06-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('178', '9', '2025-07-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('179', '9', '2025-08-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('180', '9', '2025-09-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('181', '9', '2025-10-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('182', '9', '2025-11-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('183', '9', '2025-12-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');

-- 2026 payments (4 months, all on-time)
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('184', '9', '2026-01-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('185', '9', '2026-02-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('186', '9', '2026-03-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');
INSERT INTO "LENDYR-DEMO".payment_history VALUES ('187', '9', '2026-04-19', 252.60, 0, 0, 0, 'Monthly personal loan payment');

-- Made with Bob
