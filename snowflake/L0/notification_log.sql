-- L0 raw table: Alert notification log.
-- Tracks all email alerts sent by the MAiSIGNAL system.

CREATE TABLE IF NOT EXISTS maisignal.l0.notification_log (
    id NUMBER AUTOINCREMENT,
    user_email VARCHAR NOT NULL,
    company_name VARCHAR NOT NULL,
    alert_type VARCHAR NOT NULL,
    subject VARCHAR NOT NULL,
    sent_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    status VARCHAR NOT NULL,
    ecomail_response VARCHAR
);
