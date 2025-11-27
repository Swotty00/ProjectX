CREATE TYPE sentiment AS ENUM ('positive', 'negative');

CREATE TABLE reviews(
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    texto TEXT NOT NULL,
    label sentiment NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);