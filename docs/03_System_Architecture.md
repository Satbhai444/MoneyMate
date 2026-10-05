# System Architecture

## 1. High-Level Architecture Diagram
The architecture is divided into three core tiers:
1. **Client Tier:** Telegram App (iOS, Android, Desktop) & Web Browser (Landing Page).
2. **Logic Tier:** Node.js Webhook Server & AI Parser (LLM).
3. **Data Tier:** PostgreSQL Database & Cloud Storage.

## 2. Components
### 2.1 Web & Landing Page
- Hosted on Vercel.
- Built using vanilla HTML, CSS, and JS (Zero-dependency architecture).
- Focuses on SEO, fast load times, and explaining product features through interactive DOM simulations.

### 2.2 Telegram Bot Webhook
- A Node.js (Express or serverless function) endpoint that receives POST requests from the Telegram API.
- Handles user authentication (via Telegram ID).
- Routes messages (Text/Voice) to the AI Parser.

### 2.3 AI NLP Parser
- Uses an LLM (e.g., Gemini or OpenAI) via system prompts.
- Takes unstructured text and returns a strictly formatted JSON object containing `intent`, `amount`, `category`, and `person`.
- Converts voice notes to text using Whisper API or Telegram's native voice recognition before parsing.

### 2.4 Database (PostgreSQL)
- Relational database to ensure ACID compliance for financial records.
- Stores user profiles, ledger entries, and categorized expenses.

## 3. Data Flow
1. User sends message in Telegram.
2. Telegram API forwards message to Webhook.
3. Webhook sends text to LLM for parsing.
4. LLM returns JSON structured data.
5. Webhook writes data to PostgreSQL.
6. Webhook replies to user via Telegram API with a confirmation message.
