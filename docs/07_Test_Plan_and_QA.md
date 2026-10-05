# Test Plan and QA

## 1. Testing Strategy
Given the conversational nature of Money Mate, testing primarily focuses on NLP parsing accuracy and webhook reliability.

## 2. Unit Testing
- **NLP Parsing Engine:** Feed 100+ sample sentences in mixed languages to the parsing function to ensure it outputs correct JSON.
  - *Example Case 1:* "Chai 20 rupaye" -> Expected: `expense`, `20`, `Food & Drinks`.
  - *Example Case 2:* "Kal rahul ne 500 diye" -> Expected: `settlement`, `500`, `Rahul`.
- **Database Schema Constraints:** Verify that negative amounts are rejected, and missing user IDs throw Foreign Key errors.

## 3. Integration Testing
- **End-to-End Webhook:** Mock a Telegram POST payload and send it to the local `/webhook` endpoint. Verify that the server responds with HTTP 200 and a database entry is created.
- **Voice Pipeline:** Upload a sample `.ogg` file mimicking Telegram's format and verify that STT -> LLM -> DB pipeline functions without timeouts.

## 4. User Acceptance Testing (UAT)
- Beta users will interact with the bot in a staging environment.
- Feedback on the bot's tone, accuracy, and response times will be collected.

## 5. Performance and Load Testing
- Simulate 1,000 concurrent webhook requests using Apache JMeter to ensure the Node.js server and database connection pool can handle traffic spikes without crashing.
