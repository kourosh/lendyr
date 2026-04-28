# Invoice Upload - Quick Start Guide

## How to Pay a Bill from an Invoice

### Step 1: Authenticate
```
You: Hi, I need to pay a bill
Lena: [Requests authentication]
You: My customer ID is 846301 and PIN is 93810
Lena: Welcome, Alice Martinez!
```

### Step 2: Upload Invoice
**Option A: Attach file first, then mention it**
```
1. Click the paperclip icon in the chat
2. Select your invoice file (PDF or image)
3. Type: "Here's my invoice" or "I have an invoice to pay"
4. Send the message
```

**Option B: Mention invoice first, then upload**
```
You: I have an invoice I'd like to upload
Lena: [Calls invoice_extraction_flow tool]
Lena: Please click the 'Upload files' button and select your invoice
You: [Click the upload button and select file]
```

### Step 3: Review Extracted Information
After upload, Lena will:
1. Process the invoice with AI extraction
2. Display extracted payment details
3. If any field has low confidence (<70%), you'll see a review form to verify/correct

### Step 4: Select Payment Account
```
Lena: Which account would you like to pay from?
You: My checking account
```

### Step 5: Confirm Payment
Lena will:
1. Verify sufficient funds
2. Create the payment
3. Generate a check number (CHK#####)
4. Confirm delivery estimate (5-7 business days)

## What Gets Extracted from Your Invoice

The AI automatically extracts:
- **Payee Name**: Who to pay (e.g., "ABC Electric Company")
- **Payee Address**: Where to mail the check
- **Amount Due**: How much to pay
- **Invoice Number**: For your records
- **Due Date**: Payment deadline

## Supported File Types

✅ **PDF files** (.pdf)
✅ **Images** (.jpg, .jpeg, .png)
✅ **Maximum size**: 8 MB

## Tips for Best Results

1. **Clear, readable invoices work best**
   - Avoid blurry or low-quality scans
   - Ensure text is legible

2. **Standard invoice formats**
   - Most utility bills, service invoices work well
   - Handwritten invoices may need manual correction

3. **Review extracted data**
   - Always verify the extracted information
   - Correct any errors before confirming payment

4. **Have your account ready**
   - Know which account you want to pay from
   - Ensure sufficient funds are available

## Troubleshooting

### Issue: "Document already uploaded" message
**Solution**: If you attached a file in chat, just say "process this invoice" or "extract payment info from this invoice"

### Issue: Upload button doesn't appear
**Solution**: Make sure you mention "invoice" or "upload" in your message

### Issue: Extraction fails or is inaccurate
**Solution**: 
1. Check if the file is clear and readable
2. Use the review form to correct any errors
3. If extraction completely fails, provide details manually

### Issue: Payment fails
**Possible causes:**
- Insufficient funds in selected account
- Invalid account selection
- System error

**Solution**: Check your account balance and try again, or contact support

## Example Conversation

```
You: Hi, my customer ID is 846301 and PIN is 93810

Lena: Welcome, Alice Martinez! How can I help you today?

You: I need to pay a bill. [Attaches invoice_core_pilates.pdf]

Lena: [Processes invoice with AI extraction]

Lena: I've extracted the following payment information:
- Payee: Core Pilates Studio
- Address: 123 Fitness Lane, San Francisco, CA 94102
- Amount: $150.00
- Invoice: INV-2026-001
- Due Date: May 1, 2026

Which account would you like to pay from?

You: My checking account

Lena: [Verifies funds and creates payment]

Lena: ✅ Payment created successfully!
- Check Number: CHK12347
- Amount: $150.00
- Payee: Core Pilates Studio
- Your checking account has been debited
- Check will be mailed in 5-7 business days
```

## Need Help?

- **Testing Guide**: See `docs/BILL_PAYMENT_TESTING_GUIDE.md`
- **Full Documentation**: See `docs/BILL_PAYMENT_IMPLEMENTATION_SUMMARY.md`
- **Support**: Contact Lendyr Bank at 1-800-LENDYR-1