# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.2.0] - 2026-03-06

### Added
- Monorepo structure with `snowflake/`, `backend/`, and `terraform/` components.
- Snowflake init scripts: database, schema, and service user creation.
- Snowflake L0 raw table `posledni_platne_hlaseni` for SUKL drug unavailability data.
- SQLFluff configuration for Snowflake dialect.
- Terraform configuration for AWS ECR repository and IAM role (least privilege).
- Component-level README files for snowflake, backend, and terraform.
- CHANGELOG.md.
- LICENSE file (proprietary).

### Changed
- Moved `send_maisignal_alert.py` to `backend/src/`.
- Moved `sukl-alert-email-real-data.html` to `backend/templates/`.
- Moved `requirements.txt` to `backend/`.
- Updated file paths in `send_maisignal_alert.py` for new directory layout.
- Updated root README.md as monorepo overview.
- Updated CLAUDE.md with full architecture description.
- Updated `.gitignore` for all three components.

## [0.1.0] - 2026-03-06

### Added
- Initial MAiSIGNAL alert system.
- Python script to send transactional email via Ecomail API.
- HTML email template with SUKL regulatory data, KPI metrics, and prescriber/pharmacy tables.
