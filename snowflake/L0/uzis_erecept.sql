-- L0 raw table: UZIS eRECEPT reimbursement data.
-- Source: UZIS (Ustav zdravotnickych informaci a statistiky CR).

CREATE TABLE IF NOT EXISTS maisignal.l0.uzis_erecept (
    icz_nazev_preskribujici VARCHAR,
    icz_nazev_vykazujici VARCHAR,
    lp_naz VARCHAR,
    celkova_uhrada_kc NUMBER(12, 2),
    atc5 VARCHAR,
    kvartal VARCHAR,
    rok NUMBER
);
