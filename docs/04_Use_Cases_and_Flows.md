# Use Cases and Flows

## 1. Use Case: Logging an Expense
**Actor:** User
**Trigger:** User sends "Bought a coffee for 150".
**Flow:**
1. System receives message.
2. AI identifies intent: `expense`.
3. AI extracts amount: `150`, category: `Food & Drinks`.
4. System saves record.
5. System replies: "✅ Saved! ₹150 logged under Food & Drinks."

## 2. Use Case: Managing IOUs (Lending)
**Actor:** User
**Trigger:** User sends "Lent 500 to Rahul for cab".
**Flow:**
1. AI identifies intent: `lent`.
2. AI extracts amount: `500`, person: `Rahul`.
3. System updates Rahul's ledger balance (+500).
4. System replies: "✅ Saved! You lent ₹500 to Rahul. He now owes you ₹500."

## 3. Use Case: Settling IOUs
**Actor:** User
**Trigger:** User sends "Rahul returned 500".
**Flow:**
1. AI identifies intent: `settlement`.
2. AI extracts person: `Rahul`, amount: `500`.
3. System checks Rahul's balance and deducts 500.
4. System replies: "✅ Settled! Rahul's balance is now ₹0."

## 4. Use Case: Requesting Summaries
**Actor:** User
**Trigger:** User sends "Show my monthly report".
**Flow:**
1. System queries DB for current month's expenses grouped by category.
2. System formats a markdown table.
3. System sends report via Telegram.

## 5. Use Case: Voice Logging
**Actor:** User
**Trigger:** User records and sends a voice note.
**Flow:**
1. System downloads the audio file from Telegram.
2. Audio is passed through a Speech-to-Text API.
3. The resulting text is passed to the AI Parser (Flow continues as Use Case 1).
