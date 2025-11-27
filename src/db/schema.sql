DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'sentiment') THEN
        CREATE TYPE sentiment AS ENUM ('positive', 'negative');
    END IF;
END
$$;

CREATE TABLE IF NOT EXISTS reviews(
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    texto TEXT NOT NULL,
    label sentiment NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);