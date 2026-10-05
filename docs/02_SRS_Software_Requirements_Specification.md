# Software Requirements Specification (SRS)

## 1. Introduction
This document specifies the software requirements for **Money Mate**, a Telegram-based AI expense tracking system.

## 2. Functional Requirements
**FR-1: Expense Logging**
- The system shall parse incoming text and voice messages to identify expense amounts, categories, and descriptions.
- The system must support categories like Food, Transport, Bills, Shopping, and Entertainment.

**FR-2: IOU & Settlement Tracking**
- The system must identify when money is lent or borrowed.
- The system must extract the person's name (e.g., "Rahul") and link the transaction to their virtual ledger.
- The system must allow users to settle IOUs (e.g., "Rahul returned my 500").

**FR-3: Multi-Language AI Parser**
- The NLP engine must accurately extract intents from English, Hindi, and Hinglish.

**FR-4: Data Retrieval & Summaries**
- The system shall generate daily, weekly, and monthly summaries on demand.
- The system must allow users to export their transaction history as a CSV file.

## 3. Non-Functional Requirements
**NFR-1: Performance**
- Message parsing and response time must be under 2 seconds.
- The landing page (hosted on Vercel) must achieve a Lighthouse score of 90+ for performance.

**NFR-2: Availability & Reliability**
- The Telegram bot webhook must maintain 99.9% uptime.
- The database must have daily automated backups.

**NFR-3: Security & Privacy**
- User data must be isolated by `user_id`.
- The system shall not sell or expose financial data to third parties.
- Users must have a `/delete_account` command that completely wipes their data from the database.

## 4. Software Interfaces
- **Telegram Bot API:** For bi-directional user communication.
- **LLM API (OpenAI / Gemini):** For intent classification and entity extraction.
- **Vercel / Cloudflare:** For hosting the static marketing and documentation website.
