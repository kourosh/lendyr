# Invoice Upload Workflow - Important Clarification

## How File Upload Works with Agentic Workflows

### The Issue
When you attach a file in the chat (using the paperclip icon), that file is uploaded to the chat system but **NOT automatically passed to the invoice extraction flow**. The agentic workflow has its own separate file upload mechanism.

### The Correct Workflow

**Step 1: Authenticate**
```
You: My customer ID is 846301 and PIN is 93810
Lena: Welcome, Alice Martinez!
```

**Step 2: Request Invoice Payment**
```
You: I need to pay a bill from an invoice
```

**Step 3: Lena Calls the Extraction Tool**
Lena will call `invoice_extraction_flow` which displays:
```
Please upload the file you want to use : document_ref

[Add files button]
```

**Step 4: Click "Add files" Button**
- Click the blue "Add files" button that appears
- Select your invoice file (PDF or image)
- The flow will process it

**Step 5: Review and Complete**
- Review extracted information
- Select payment account
- Confirm payment

## Why Chat Attachments Don't Work

The agentic workflow uses `DocumentProcessingCommonInput` which requires files to be uploaded through its own interface. This is because:

1. **Different Upload Contexts**: Chat attachments and flow inputs are separate systems
2. **Document Processing Requirements**: The flow needs the file in a specific format for AI processing
3. **Security and Validation**: The flow validates and processes files through its own pipeline

## Recommended User Experience

### Option 1: Don't Attach in Chat (Recommended)
```
You: I need to pay a bill from an invoice
Lena: [Displays upload button]
You: [Click "Add files" and select invoice]
```

### Option 2: If Already Attached (Current Limitation)
```
You: [Attaches invoice_core_pilates.pdf]
You: I need to pay this invoice
Lena: [Displays upload button - you must upload again]
You: [Click "Add files" and select the same file again]
```

## Alternative Approach: Manual Entry

If the double-upload is confusing, users can provide details manually:

```
You: I need to pay a bill
Lena: I can help with that. Please provide:
- Payee name
- Payee address  
- Amount
- Which account to pay from

You: 
- Payee: Core Pilates Studio
- Address: 123 Fitness Lane, San Francisco, CA 94102
- Amount: $150.00
- Pay from checking account

Lena: [Processes payment without needing file upload]
```

## Technical Explanation

### Why This Happens

The `invoice_extraction_flow` is defined with:
```python
@flow(
    name="invoice_extraction_flow",
    input_schema=DocumentProcessingCommonInput  # <-- Requires its own upload
)
```

`DocumentProcessingCommonInput` creates a dedicated file upload interface that's independent of the chat system. This is by design in Orchestrate's architecture.

### Potential Solutions (Future)

1. **Pre-process Chat Attachments**: Create a wrapper that detects chat attachments and passes them to the flow
2. **Hybrid Approach**: Use a different input schema that accepts both chat attachments and explicit uploads
3. **Custom Upload Handler**: Build a custom tool that bridges chat attachments to flow inputs

## Current Best Practice

**For Users:**
1. Don't attach files in chat
2. Wait for the "Add files" button from Lena
3. Click the button and select your invoice
4. Review and confirm extracted information

**For Developers:**
This is a known limitation of document processing flows in Orchestrate. The flow's upload mechanism is separate from chat attachments by design.

## Summary

- ❌ Attaching files in chat does NOT automatically upload them to the extraction flow
- ✅ Users must click the "Add files" button provided by the flow
- ✅ Alternative: Provide payment details manually without file upload
- 🔄 This is a platform limitation, not a bug in our implementation

The feature works correctly - it just requires using the flow's upload button rather than chat attachments.