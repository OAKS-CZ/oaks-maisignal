-- L0 raw table: Client ATC portfolio mapping.
-- Maps client companies to the ATC codes they are interested in monitoring.

CREATE TABLE IF NOT EXISTS maisignal.l0.client_portfolio (
    user_email VARCHAR NOT NULL,
    company_name VARCHAR NOT NULL,
    atc_portfolio VARCHAR NOT NULL
);
