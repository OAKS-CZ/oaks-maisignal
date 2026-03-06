# Snowflake — MAiSIGNAL Data Layer

Snowflake SQL scripts for the MAiSIGNAL data infrastructure.

## Data Layer Architecture

| Layer | Directory | Purpose |
|-------|-----------|---------|
| L0 | `L0_raw/` | Raw source data, no transformations |
| L1 | `L1_filtered/` | Basic filtering, renaming, convention alignment |
| L2 | `L2_joined/` | Joins across tables and codelists |
| L3 | `L3_business/` | Real-world business objects and metrics |
| L4 | `L4_viz/` | Visualization-ready aggregations and outputs |

Currently only L0 is implemented.

## Init Scripts

Execute in order against a Snowflake account with `ACCOUNTADMIN` or equivalent privileges:

```bash
snowsql -f init/01_create_database.sql
snowsql -f init/02_create_schema.sql
snowsql -f init/03_create_user.sql
```

**Important:** Edit `03_create_user.sql` and replace `<strong_password>` with a secure password before executing.

## Tables

### `maisignal.raw.posledni_platne_hlaseni`

SUKL latest valid drug unavailability reports. Source: [SUKL Open Data](https://opendata.sukl.cz/).

| Column | Type | Description |
|--------|------|-------------|
| `kod_sukl` | `NUMBER NOT NULL` | SUKL drug code (primary identifier) |
| `nazev` | `VARCHAR` | Drug name |
| `doplnek` | `VARCHAR` | Drug supplement info |
| `reg` | `VARCHAR` | Registration number |
| `atc` | `VARCHAR` | ATC classification code |
| `typ_oznameni` | `VARCHAR` | Notification type |
| `platnost_od` | `DATE` | Valid from date |
| `datum_hlaseni` | `DATE` | Report date |
| `nahrazujici_lp` | `VARCHAR` | Substitute drug |
| `nahrazujici_lp_poznamka` | `VARCHAR` | Substitute drug note |
| `duvod_preruseni_ukonceni` | `VARCHAR` | Reason for interruption/termination |
| `termin_obnoveni` | `DATE` | Expected recovery date |

## Linting

```bash
sqlfluff lint .
```

Configuration is in `.sqlfluff` (dialect: `snowflake`).
