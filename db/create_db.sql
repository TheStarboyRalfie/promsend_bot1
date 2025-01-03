CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    tariff TEXT NOT NULL,
    tariff_ends TIMESTAMP NOT NULL,
    ad_text TEXT NOT NULL,
    ad_photo TEXT DEFAULT 'no_photo',
    promocode TEXT DEFAULT 'no_code'
);
CREATE TABLE promocodes (
    id SERIAL PRIMARY KEY,
    code_name TEXT NOT NULL,
    discount NUMERIC NOT NULL
);