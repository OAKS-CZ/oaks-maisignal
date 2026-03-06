"""MAiSIGNAL – Send transactional email alert via Ecomail API."""

import json
import logging
import os
import sys
from pathlib import Path

import requests
import snowflake.connector
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

BACKEND_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BACKEND_DIR / "config" / ".env"
HTML_FILE = BACKEND_DIR / "templates" / "sukl-alert-email-real-data.html"
ECOMAIL_URL = "https://api2.ecomailapp.cz/transactional/send-message"


def load_config(env_path: Path = ENV_PATH) -> str:
    """Load .env (if exists) and return the ECOMAIL_API_KEY.

    The .env file is optional — the API key can also be set as an
    environment variable directly (e.g. via ``docker run -e``).

    Raises:
        ValueError: If ECOMAIL_API_KEY is not set.
    """
    if env_path.is_file():
        load_dotenv(env_path)
        logger.info("Loaded .env from %s", env_path)

    api_key = os.getenv("ECOMAIL_API_KEY")
    if not api_key:
        raise ValueError("ECOMAIL_API_KEY is not set.")
    return api_key


SNOWFLAKE_ENV_VARS = [
    "SNOWFLAKE_ACCOUNT",
    "SNOWFLAKE_USER",
    "SNOWFLAKE_PASSWORD",
    "SNOWFLAKE_ROLE",
    "SNOWFLAKE_WAREHOUSE",
]


def load_snowflake_config(env_path: Path = ENV_PATH) -> dict:
    """Load Snowflake connection parameters from environment variables.

    Raises:
        ValueError: If any required Snowflake env var is missing.
    """
    if env_path.is_file():
        load_dotenv(env_path)

    missing = [v for v in SNOWFLAKE_ENV_VARS if not os.getenv(v)]
    if missing:
        raise ValueError(
            f"Missing Snowflake env vars: {', '.join(missing)}"
        )

    return {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "user": os.getenv("SNOWFLAKE_USER"),
        "password": os.getenv("SNOWFLAKE_PASSWORD"),
        "role": os.getenv("SNOWFLAKE_ROLE"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    }


def fetch_recipients(sf_config: dict) -> list[dict]:
    """Fetch email recipients from the Snowflake client_portfolio table.

    Returns:
        List of dicts with ``email`` and ``name`` keys.

    Raises:
        RuntimeError: If no recipients are found.
    """
    conn = snowflake.connector.connect(**sf_config)
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT user_email, company_name "
            "FROM maisignal.l0.client_portfolio"
        )
        rows = cur.fetchall()
    finally:
        conn.close()

    if not rows:
        raise RuntimeError("No recipients found in client_portfolio.")

    return [{"email": row[0], "name": row[1]} for row in rows]


def load_template(template_path: Path = HTML_FILE) -> str:
    """Read and return the HTML email template.

    Raises:
        FileNotFoundError: If the template file does not exist.
    """
    if not template_path.is_file():
        raise FileNotFoundError(f"HTML template not found: {template_path}")
    html = template_path.read_text(encoding="utf-8")
    logger.info("Loaded HTML template (%d chars).", len(html))
    return html


def build_payload(html_content: str, recipient: dict) -> dict:
    """Build the Ecomail transactional email payload."""
    return {
        "message": {
            "subject": (
                "\u26a0\ufe0f MAiSIGNAL: V\u00fdpadek LP"
                " \u2013 LYRICA (Pregabalin)"
            ),
            "from_name": "MAiSIGNAL Alerts",
            "from_email": "alerts@mailing.oaks.cz",
            "reply_to": "noreply@mailing.oaks.cz",
            "to": [
                {
                    "email": recipient["email"],
                    "name": recipient["name"],
                }
            ],
            "html": html_content,
            "text": (
                "MAiSIGNAL Alert - Vypadek LP: LYRICA (Pregabalin). "
                "Duvod: Preruseni dodavky. Platnost od: 2025-01-01. "
                "Zdroj: SUKL - Hlaseni nedostupnosti. "
                "Vice informaci v HTML verzi emailu."
            ),
            "options": {
                "click_tracking": True,
                "open_tracking": True,
            },
        }
    }


def send_alert(
    payload: dict,
    api_key: str,
    url: str = ECOMAIL_URL,
) -> requests.Response:
    """POST the payload to the Ecomail transactional API.

    Returns:
        The :class:`requests.Response` object.
    """
    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "key": api_key,
        },
        data=json.dumps(payload),
        timeout=30,
    )
    return response


def main() -> None:
    """Orchestrate config loading, template reading, and alert sending."""
    try:
        api_key = load_config()
    except ValueError as exc:
        logger.error(str(exc))
        sys.exit(1)

    try:
        html_content = load_template()
    except FileNotFoundError as exc:
        logger.error(str(exc))
        sys.exit(1)

    try:
        sf_config = load_snowflake_config()
    except ValueError as exc:
        logger.error(str(exc))
        sys.exit(1)

    try:
        recipients = fetch_recipients(sf_config)
    except RuntimeError as exc:
        logger.error(str(exc))
        sys.exit(1)

    logger.info("Sending alerts to %d recipients...", len(recipients))
    failures = 0

    for recipient in recipients:
        payload = build_payload(html_content, recipient)
        try:
            response = send_alert(payload, api_key)
        except requests.RequestException as exc:
            logger.error(
                "Network error sending to %s: %s", recipient["email"], exc
            )
            failures += 1
            continue

        logger.info(
            "Response for %s: %d", recipient["email"], response.status_code
        )

        if not response.ok:
            logger.error(
                "Ecomail API error for %s: %s",
                recipient["email"],
                response.text,
            )
            failures += 1
            continue

        logger.info("Alert sent to %s.", recipient["email"])

    if failures:
        logger.error("%d of %d sends failed.", failures, len(recipients))
        sys.exit(1)

    logger.info("All %d alerts sent successfully.", len(recipients))


if __name__ == "__main__":
    main()
