CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    username TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS expenses (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    amount NUMERIC(12, 2) NOT NULL CHECK (amount >= 0),
    category TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS habits (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    reminder_month SMALLINT NOT NULL DEFAULT 1 CHECK (reminder_month BETWEEN 1 AND 12),
    reminder_day SMALLINT NOT NULL DEFAULT 1 CHECK (reminder_day BETWEEN 1 AND 31),
    reminder_hour SMALLINT NOT NULL DEFAULT 9 CHECK (reminder_hour BETWEEN 0 AND 23),
    last_notified_year INTEGER,
    frequency TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS shopping_items (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS note_categories (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, title)
);

CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES note_categories(id) ON DELETE SET NULL,
    body TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Legacy compatibility for older handlers still writing into tasks/frequency.
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    deadline DATE,
    is_done BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE habits ADD COLUMN IF NOT EXISTS reminder_month SMALLINT;
ALTER TABLE habits ADD COLUMN IF NOT EXISTS reminder_day SMALLINT;
ALTER TABLE habits ADD COLUMN IF NOT EXISTS reminder_hour SMALLINT;
ALTER TABLE habits ADD COLUMN IF NOT EXISTS last_notified_year INTEGER;
ALTER TABLE habits ADD COLUMN IF NOT EXISTS frequency TEXT;

UPDATE habits SET reminder_month = COALESCE(reminder_month, 1);
UPDATE habits SET reminder_day = COALESCE(reminder_day, 1);
UPDATE habits SET reminder_hour = COALESCE(reminder_hour, 9);
