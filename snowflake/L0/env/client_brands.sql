-- L0 env table: Client brand mapping (per-environment).
-- Maps client companies to the brand names of their products.

CREATE TABLE IF NOT EXISTS maisignal.l0_dev.client_brands (
    user_email VARCHAR NOT NULL,
    company_name VARCHAR NOT NULL,
    brand VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS maisignal.l0_prod.client_brands (
    user_email VARCHAR NOT NULL,
    company_name VARCHAR NOT NULL,
    brand VARCHAR NOT NULL
);
