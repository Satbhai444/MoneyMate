PROJECT BRIEF: MoneyMate (college semester project)
Title: "MoneyMate: AI Expense Manager Chatbot for Telegram"

WHAT IT IS
A Telegram bot (@HeyMoneyMate_bot) where a user logs expenses, income and udhaar
(money lent/borrowed) by chatting normally in English or Hinglish, e.g.
"20 ki water bottle", "500 dinner", "aaj 1000 Rahul ko diye", "Rahul ne 800 wapis diye".
Every entry is saved with exact date and time. Bot and web dashboard share ONE Supabase
database, so entries appear on the web instantly. When the user asks for the monthly report,
the bot sends a private dashboard link.

CURRENT STATE
- Landing website is DONE and live: https://moneymate-website.vercel.app (plain HTML/CSS/JS).
  Do not redesign it. Only touch it where a task below says so.
- Telegram bot is created on BotFather (username @HeyMoneyMate_bot, description, commands,
  profile photo set). Token is in .env (never print, log or commit it).
- Supabase project is created with tables: users(id, telegram_id, name, dashboard_token,
  created_at) and transactions(id, user_id, type, amount, category, person, note,
  created_at, deleted_at). type = expense | income | lent | borrowed | settle_received |
  settle_paid. Deletes are soft (deleted_at).
- FIRST STEP: inspect the repo and tell me what already exists (bot.py, parser, db layer,
  dashboard). Do not rebuild anything that already works. List what is missing, then continue.

KEYS (in .env only): TELEGRAM_BOT_TOKEN, GEMINI_API_KEY, SUPABASE_URL,
SUPABASE_SERVICE_KEY, DASHBOARD_BASE_URL. Provide .env.example. .env must be in .gitignore.

REMAINING WORK, IN THIS ORDER (finish and test each before the next)

1. BOT BACKEND (Python 3.11, python-telegram-bot v21 async, supabase-py, google-genai
   with gemini-2.5-flash, pydantic, timezone Asia/Kolkata, currency INR)
   - /start: upsert user by telegram_id, welcome message, inline menu.
   - /menu: inline buttons (Add Expense, Add Income, Split, Who Owes, Monthly Report, Undo).
     Button taps run plain logic from callback_data, no AI. Add and Split ask a follow-up
     question and treat the next message as the answer (ConversationHandler).
   - Free text: send to Gemini parser, validate JSON, save with SERVER time (never let AI
     choose the date). Reply like: "✅ ₹500 · Food · Dinner saved - 05 Oct, 2:04 PM"
     with [Undo] [Report] buttons.
   - If parser says needs_clarification, ask its question and finish the entry from the reply.
   - /owed: per person pending = (lent - settle_received) and (borrowed - settle_paid).
     Calculate in code/SQL, never with AI.
   - /undo: soft delete the user's latest entry.
   - /report: send DASHBOARD_BASE_URL/d/<dashboard_token> plus a quick summary
     (month total, top 3 categories). Also trigger on text like "monthly report".
   - Parser output JSON: intent, amount, category (Food|Travel|Bills|Shopping|Health|
     Entertainment|Other), person, note, needs_clarification, question. Use JSON mode.
     Put 12+ few-shot examples in the prompt (English + Hinglish). Mapping:
     "Rahul ko 1000 diye" = lent; "Rahul ne 800 wapis diye" = settle_received;
     "maine Rahul ko 300 wapis diye" = settle_paid; "Rahul se 200 liye" = borrowed.
   - Friendly error messages, logging, 20 messages/min rate limit per user.
   - tests/test_parser.py with 15 sample sentences.

2. WEB DASHBOARD (Next.js, separate folder, deploy on Vercel)
   - Route /d/[token]: server side looks up the user by dashboard_token using the service key
     (service key must NEVER reach the browser). Invalid token = clean "link invalid" page.
   - Show: month selector, total spent, total income, category breakdown chart,
     daily spending chart, full transaction list with exact date and time, and an
     Udhaar section (per person: lent, received back, pending).
   - Realtime: new entries from the bot appear without refresh (poll every 10 s is fine).
   - CSV export button. Mobile-first, dark and light mode, same monochrome look as the landing
     site (black/white, one red accent, dot-matrix style headings).
   - Add a Vercel env var for SUPABASE_URL and SUPABASE_SERVICE_KEY (server only).

3. DEPLOY THE BOT
   - Bot must run 24/7, not on my laptop. Switch to webhook mode (FastAPI + python-telegram-bot)
     and deploy on Render (free web service) or Railway. Set the webhook with setWebhook and a
     secret token header. Add a /health endpoint.
   - Set DASHBOARD_BASE_URL to the deployed dashboard URL.

4. CONNECT EVERYTHING
   - Landing site: confirm "Open Telegram" buttons point to https://t.me/HeyMoneyMate_bot.
     Add a small "Monthly dashboard" section and a "Try the parser" demo only if it is not
     already there. Do not break existing links.
   - End-to-end test: /start, "20 ki water bottle", "aaj 1000 Rahul ko diye",
     "Rahul ne 800 wapis diye", /owed (must show ₹200), /report (link opens dashboard with
     the same entries), /undo.

5. DOCS FOR SUBMISSION
   - README.md: overview, architecture diagram (text), setup steps, env vars, how to run,
     screenshots placeholders.
   - docs/ARCHITECTURE.md: Telegram -> webhook -> Gemini parser -> Supabase <- dashboard.
   - docs/DEMO_SCRIPT.md: 2-minute demo flow with exact messages to type.

RULES
- Never print or commit secrets. If a secret appears in output, stop and tell me.
- Keep it simple: no extra frameworks or services beyond those named above.
- After each step, summarize what changed and how I can test it.
- Ask me only if something blocks you; otherwise make the sensible choice and note it.