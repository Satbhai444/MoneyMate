# API and Integrations

## 1. Telegram Bot API
The primary interface for user interaction.
- **Endpoint:** `api.telegram.org/bot<TOKEN>/setWebhook`
- **Webhook Implementation:** The backend exposes a `/webhook` POST route.
- **Message Types Handled:** 
  - `message.text`
  - `message.voice`

## 2. LLM Integration (Intent Extraction)
The backend uses a Large Language Model (e.g., Gemini 1.5 Flash or OpenAI GPT-4o-mini) to extract structured data from unstructured text.

**System Prompt Example:**
```text
You are a financial parsing assistant. The user will provide a sentence in English, Hindi, or Hinglish.
Extract the intent (expense, income, lent, borrowed), amount (as a number), category, and person's name (if applicable).
Respond ONLY with a valid JSON object.
```

## 3. Speech-to-Text (STT) Integration
When a user sends a voice note (`message.voice`), the backend:
1. Calls `getFile` on the Telegram API to get the audio file path.
2. Downloads the `.ogg` file.
3. Sends the file to an STT API (e.g., OpenAI Whisper).
4. Forwards the transcribed text to the LLM Integration (Step 2).

## 4. Frontend Integrations
The Vercel-hosted landing page does not directly interact with the backend API to ensure complete decoupling. The frontend relies exclusively on native DOM APIs and handles its own local interactive simulation using Regex.
