-- L0 raw table: Client brand mapping.
-- Maps client companies to the brand names of their products.

CREATE TABLE IF NOT EXISTS maisignal.l0.client_brands (
    user_email VARCHAR NOT NULL,
    company_name VARCHAR NOT NULL,
    brand VARCHAR NOT NULL
);
