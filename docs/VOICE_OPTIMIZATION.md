# Voice Channel Optimization Guide

## Overview

All Lendyr Bank AI agents have been enhanced with voice channel optimization to provide concise, natural responses when customers interact through voice or phone channels, while maintaining detailed responses for text/chat channels.

## Architecture Decision

**Single Agent Architecture**: We modified the existing agents rather than creating separate voice-only agents. This approach:
- ✅ Maintains a single source of truth for business logic
- ✅ Avoids agent confusion and routing complexity
- ✅ Simplifies maintenance and updates
- ✅ Provides better responsiveness through context-aware behavior

## How It Works

Each agent checks the communication channel from the context and adapts its response style:

- **Voice/Phone Channels**: Concise, spoken-friendly responses
- **Text/Chat Channels**: Detailed, formatted responses with tables and full information

## Agent-Specific Optimizations

### 1. Lendyr Customer Care (Lena)

**Voice Channel Behavior:**
- Brief, natural greetings: "Hi, I'm Lena from Lendyr Bank. How can I help you today?"
- Conversational authentication: "I'll need your customer ID and PIN to get started"
- Avoids lengthy explanations or reading lists of options

**Text Channel Behavior:**
- Standard detailed greetings and instructions
- Full authentication protocol explanations

### 2. Account Agent

**Voice Channel Behavior:**
- Summarizes account balances concisely
- Example: "You have $500 in checking, $250 in savings, and you owe $5,000 on your credit card"
- Avoids reading account numbers digit-by-digit unless requested
- Skips visual formatting like tables

**Text Channel Behavior:**
- Presents ALL accounts in clear table format
- Shows account type, account number, and balance
- Never combines or summarizes

### 3. Loan Agent

**Voice Channel Behavior:**
- Focuses on key details: "Your auto loan has a balance of $15,000. Your next payment of $450 is due on March 15th"
- Avoids reading every field unless specifically asked
- States dispute status and next steps concisely

**Text Channel Behavior:**
- Full loan details with all fields
- Formatted amounts, dates, and percentages
- Complete payment history and dispute information

### 4. Card Agent

**Voice Channel Behavior:**
- Summarizes cards: "You have a Visa debit card ending in 1234 and a Mastercard credit card ending in 5678"
- Avoids reading full card numbers unless requested
- Brief confirmations: "I've frozen your Visa debit card. You can unfreeze it anytime"

**Text Channel Behavior:**
- Full card details with all fields
- Detailed confirmation messages
- Complete status explanations

### 5. Loan Deferral Agent

**Voice Channel Behavior:**
- Concise eligibility results: "Good news, you qualify for a 30-day deferral"
- Summarizes key terms: "Your next payment moves to March 15th, and $45 in interest will be added to your balance"
- Short confirmations: "All set, your deferral is processed. Your next payment is March 15th"

**Text Channel Behavior:**
- Full detailed explanations of eligibility criteria
- Complete breakdown of calculations
- Detailed terms and conditions

## Implementation Details

### Channel Detection

Agents check the communication channel from the context variables provided by watsonx Orchestrate:

```yaml
VOICE CHANNEL OPTIMIZATION:
Check the communication channel from context. If the channel is "voice" or "phone":
  - [voice-specific instructions]

For text/chat channels:
  - [text-specific instructions]
```

### Response Guidelines for Voice Channels

1. **Be Concise**: Summarize key information without reading every detail
2. **Use Natural Language**: Speak conversationally, not like reading a form
3. **Avoid Visual Formatting**: No tables, bullet points, or complex structures
4. **Focus on Key Information**: Highlight what matters most to the customer
5. **Skip Redundancy**: Don't repeat information unless asked

### Response Guidelines for Text Channels

1. **Be Comprehensive**: Provide all relevant details
2. **Use Formatting**: Tables, bullet points, and clear structure
3. **Show All Data**: Don't summarize or omit information
4. **Be Precise**: Include exact numbers, dates, and account details

## Testing Recommendations

### Voice Channel Testing

Test with these scenarios:
1. "What are my account balances?" - Should get concise summary
2. "Tell me about my loan" - Should get key details only
3. "What cards do I have?" - Should get brief card list

### Text Channel Testing

Test with the same scenarios:
1. "What are my account balances?" - Should get full table
2. "Tell me about my loan" - Should get all loan details
3. "What cards do I have?" - Should get complete card information

## Deployment

All agents have been updated with voice optimization. To deploy:

```bash
# Deploy all agents to draft environment
./scripts/import_all_to_lendyr_cloud.sh

# Test in draft environment with both voice and text channels

# Promote to live when testing is complete
```

## Benefits

1. **Better Voice Experience**: Customers get quick, natural responses suitable for listening
2. **Maintained Text Experience**: Chat users still get comprehensive, detailed information
3. **Single Codebase**: Easier to maintain and update
4. **Context-Aware**: Agents automatically adapt to the communication channel
5. **No Agent Confusion**: Single routing logic, no duplicate agents

## Future Enhancements

Potential improvements:
- Add SSML markup for voice synthesis control (pauses, emphasis)
- Implement voice-specific error handling
- Add voice-optimized confirmation flows
- Support for multi-turn voice conversations with context retention

## Support

For questions or issues with voice optimization:
- Review agent YAML files in `/agents` directory
- Check watsonx Orchestrate documentation for channel context variables
- Test in draft environment before promoting to live