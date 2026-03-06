-- L0 env table: Client ATC portfolio mapping (per-environment).
-- Maps client companies to the ATC codes they are interested in monitoring.

CREATE TABLE IF NOT EXISTS maisignal.l0_dev.client_portfolio (
    user_email VARCHAR NOT NULL,
    company_name VARCHAR NOT NULL,
    atc_portfolio VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS maisignal.l0_prod.client_portfolio (
    user_email VARCHAR NOT NULL,
    company_name VARCHAR NOT NULL,
    atc_portfolio VARCHAR NOT NULL
);
