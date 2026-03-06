"""Snowflake adapter for fetching email recipients."""

import logging

from snowflake.connector import SnowflakeConnection

from maisignal.domain.models import Recipient

logger = logging.getLogger(__name__)

ALLOWED_SCHEMAS = ("l0", "l0_dev", "l0_prod")


class SnowflakeRecipientRepository:
    """Fetches recipients from the Snowflake client_portfolio table."""

    def __init__(
        self, connection: SnowflakeConnection, schema: str = "l0"
    ) -> None:
        if schema not in ALLOWED_SCHEMAS:
            raise ValueError(
                f"Invalid schema '{schema}'. "
                f"Allowed: {', '.join(ALLOWED_SCHEMAS)}"
            )
        self._conn = connection
        self._query = (
            f"SELECT user_email, company_name "
            f"FROM maisignal.{schema}.client_portfolio"
        )

    def get_all(self) -> list[Recipient]:
        """Query recipients and return them.

        Raises:
            RuntimeError: If no recipients are found.
        """
        cur = self._conn.cursor()
        cur.execute(self._query)
        rows = cur.fetchall()

        if not rows:
            raise RuntimeError("No recipients found in client_portfolio.")

        recipients = [Recipient(email=row[0], name=row[1]) for row in rows]
        logger.info("Fetched %d recipients from Snowflake.", len(recipients))
        return recipients
