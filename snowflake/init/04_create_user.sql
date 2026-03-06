-- Create service account user and role for MAiSIGNAL.
-- Replace <strong_password> with a secure password before executing.

CREATE ROLE IF NOT EXISTS maisignal_svc_role;

CREATE USER IF NOT EXISTS maisignal_svc
    PASSWORD = '<strong_password>'
    DEFAULT_ROLE = maisignal_svc_role
    DEFAULT_WAREHOUSE = maisignal_wh
    MUST_CHANGE_PASSWORD = FALSE;

-- Grant warehouse access.
GRANT USAGE ON WAREHOUSE maisignal_wh TO ROLE maisignal_svc_role;

-- Grant database and schema access.
GRANT USAGE ON DATABASE maisignal TO ROLE maisignal_svc_role;
GRANT USAGE ON SCHEMA maisignal.l0 TO ROLE maisignal_svc_role;

-- Grant table-level privileges.
GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA maisignal.l0 TO ROLE maisignal_svc_role;
GRANT SELECT, INSERT ON FUTURE TABLES IN SCHEMA maisignal.l0 TO ROLE maisignal_svc_role;

-- Grant access to per-environment schemas.
GRANT USAGE ON SCHEMA maisignal.l0_dev TO ROLE maisignal_svc_role;
GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA maisignal.l0_dev TO ROLE maisignal_svc_role;
GRANT SELECT, INSERT ON FUTURE TABLES IN SCHEMA maisignal.l0_dev TO ROLE maisignal_svc_role;

GRANT USAGE ON SCHEMA maisignal.l0_prod TO ROLE maisignal_svc_role;
GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA maisignal.l0_prod TO ROLE maisignal_svc_role;
GRANT SELECT, INSERT ON FUTURE TABLES IN SCHEMA maisignal.l0_prod TO ROLE maisignal_svc_role;

-- Assign role to user.
GRANT ROLE maisignal_svc_role TO USER maisignal_svc;
