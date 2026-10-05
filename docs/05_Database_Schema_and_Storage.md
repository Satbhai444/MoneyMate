# Database Schema and Storage

## 1. Overview
The database uses a relational model (PostgreSQL) to ensure data integrity and fast querying for reports.

## 2. Tables

### 2.1 Users Table
Stores information about the Telegram users interacting with the bot.
- `id` (UUID, Primary Key)
- `telegram_id` (BigInt, Unique) - From Telegram API
- `username` (Varchar, Nullable)
- `first_name` (Varchar)
- `created_at` (Timestamp, Default NOW())
- `currency_pref` (Varchar, Default 'INR')

### 2.2 Transactions Table
Stores individual expenses and incomes.
- `id` (UUID, Primary Key)
- `user_id` (UUID, Foreign Key -> Users.id)
- `type` (Enum: 'expense', 'income')
- `amount` (Decimal)
- `category` (Varchar)
- `description` (Text, Nullable)
- `date` (Date, Indexed for fast queries)
- `created_at` (Timestamp)

### 2.3 Ledger (IOUs) Table
Tracks money lent and borrowed between the user and third parties.
- `id` (UUID, Primary Key)
- `user_id` (UUID, Foreign Key -> Users.id)
- `person_name` (Varchar) - The name of the friend (e.g., 'Rahul')
- `type` (Enum: 'lent', 'borrowed')
- `amount` (Decimal)
- `status` (Enum: 'pending', 'settled')
- `settled_on` (Date, Nullable)
- `created_at` (Timestamp)

## 3. Data Privacy and Security
- All user identifiers (`telegram_id`) must be strictly bound to their respective rows. Row-Level Security (RLS) is applied to ensure cross-user data leakage is impossible.
- Financial data is encrypted at rest by the cloud provider.
