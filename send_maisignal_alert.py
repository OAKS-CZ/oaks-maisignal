"""MAiSIGNAL – Send transactional email alert via Ecomail API."""

import json
import logging
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

SCRIPT_DIR = Path(__file__).resolve().parent
ENV_PATH = SCRIPT_DIR / "config" / ".env"
HTML_FILE = SCRIPT_DIR / "sukl-alert-email-real-data.html"
ECOMAIL_URL = "https://api2.ecomailapp.cz/transactional/send-message"


def main() -> None:
    if not ENV_PATH.is_file():
        logger.error("config/.env not found. Create it with ECOMAIL_API_KEY.")
        sys.exit(1)

    load_dotenv(ENV_PATH)
    api_key = os.getenv("ECOMAIL_API_KEY")

    if not api_key:
        logger.error("ECOMAIL_API_KEY is not set in config/.env.")
        sys.exit(1)

    if not HTML_FILE.is_file():
        logger.error("HTML template not found: %s", HTML_FILE)
        sys.exit(1)

    html_content = HTML_FILE.read_text(encoding="utf-8")
    logger.info("Loaded HTML template (%d chars).", len(html_content))

    payload = {
        "message": {
            "subject": "⚠️ MAiSIGNAL: Výpadek LP – LYRICA (Pregabalin)",
            "from_name": "MAiSIGNAL Alerts",
            "from_email": "alerts@mailing.oaks.cz",
            "reply_to": "noreply@mailing.oaks.cz",
            "to": [
                {
                    "email": "marko.sidlovsky@oaks.cz",
                    "name": "Marko Sidlovsky",
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

    logger.info("Sending alert via Ecomail API...")
    response = requests.post(
        ECOMAIL_URL,
        headers={
            "Content-Type": "application/json",
            "key": api_key,
        },
        data=json.dumps(payload),
        timeout=30,
    )

    logger.info("Response status: %d", response.status_code)
    logger.info("Response body: %s", response.text)

    if not response.ok:
        logger.error("Ecomail API returned an error.")
        sys.exit(1)

    logger.info("Alert sent successfully.")


if __name__ == "__main__":
    main()
