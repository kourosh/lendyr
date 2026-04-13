# Proposed Payment Histories for Lendyr Customers

## Summary
Creating payment histories for 5 customers to demonstrate different payment patterns.

---

## 1. **Carla Thompson** (Customer ID: 3, Loan ID: 2)
- **Loan Type:** Mortgage
- **Monthly Payment:** $5,363.33
- **Payment History:** 28 payments total
  - **26 on-time payments** (status: 'on_time', days_late: 0)
  - **2 late payments** (status: 'late', days_late: 5 and 12)
- **Period:** January 2024 - April 2026 (28 months)
- **Late Payment Months:** March 2025 (5 days late), September 2025 (12 days late)
- **Credit Score:** 680 (fair - explains occasional late payments)

---

## 2. **Elena Okafor** (Customer ID: 5, Loan ID: 3)
- **Loan Type:** Personal Loan
- **Monthly Payment:** $252.60
- **Payment History:** 24 payments total
  - **24 on-time payments** (all status: 'on_time', days_late: 0)
- **Period:** May 2024 - April 2026 (24 months)
- **Credit Score:** 725 (good - consistent on-time payments)

---

## 3. **Frank Rossi** (Customer ID: 6, Loan ID: 4)
- **Loan Type:** Mortgage
- **Monthly Payment:** $5,363.33
- **Payment History:** 18 payments total
  - **17 on-time payments** (status: 'on_time', days_late: 0)
  - **1 late payment** (status: 'late', days_late: 8)
- **Period:** November 2024 - April 2026 (18 months)
- **Late Payment Month:** February 2025 (8 days late)
- **Credit Score:** 695 (good - mostly reliable)

---

## 4. **Henry Williams** (Customer ID: 8, Loan ID: 5)
- **Loan Type:** Auto Loan
- **Monthly Payment:** $469.35
- **Payment History:** 12 payments total
  - **10 on-time payments** (status: 'on_time', days_late: 0)
  - **2 late payments** (status: 'late', days_late: 15 and 22)
- **Period:** May 2025 - April 2026 (12 months)
- **Late Payment Months:** August 2025 (15 days late), December 2025 (22 days late)
- **Credit Score:** 650 (fair - some payment issues)

---

## 5. **Isabela Cruz** (Customer ID: 9, Loan ID: 6)
- **Loan Type:** Personal Loan
- **Monthly Payment:** $252.60
- **Payment History:** 30 payments total
  - **30 on-time payments** (all status: 'on_time', days_late: 0)
- **Period:** November 2023 - April 2026 (30 months)
- **Credit Score:** 788 (excellent - perfect payment history)

---

## Payment ID Allocation
- Brian Nguyen already uses payment_id 1-75 (45 payments + 30 from existing data)
- New payment IDs will start from **76** onwards
- Total new payments: 28 + 24 + 18 + 12 + 30 = **112 new payment records**
- Payment IDs: **76 through 187**

---

## Rationale
1. **Variety of patterns:** Mix of perfect payers (Elena, Isabela) and those with occasional issues (Carla, Frank, Henry)
2. **Realistic timing:** Different loan start dates to reflect real-world scenarios
3. **Credit score alignment:** Payment histories match their credit scores
4. **Different loan types:** Coverage across mortgage, personal, and auto loans
5. **As requested:** Carla has 28 payments with 2 late, others provide additional variety