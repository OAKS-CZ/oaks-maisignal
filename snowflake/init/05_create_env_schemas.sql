-- Create per-environment schemas for client data isolation.

USE DATABASE maisignal;
CREATE SCHEMA IF NOT EXISTS l0_dev;
CREATE SCHEMA IF NOT EXISTS l0_prod;
