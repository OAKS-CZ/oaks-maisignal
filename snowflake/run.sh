#!/usr/bin/env bash
# SnowSQL runner — executes SQL files against Snowflake.
# Usage: ./run.sh <file_or_directory>
#
# Loads credentials from snowflake/config/.env.
# If a directory is given, all .sql files are executed in sorted order.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/config/.env"

if [[ ! -f "${ENV_FILE}" ]]; then
    echo "Error: ${ENV_FILE} not found." >&2
    echo "Create it with: SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ROLE, SNOWFLAKE_WAREHOUSE" >&2
    exit 1
fi

# shellcheck source=/dev/null
source "${ENV_FILE}"

for var in SNOWFLAKE_ACCOUNT SNOWFLAKE_USER SNOWFLAKE_PASSWORD SNOWFLAKE_ROLE SNOWFLAKE_WAREHOUSE; do
    if [[ -z "${!var:-}" ]]; then
        echo "Error: ${var} is not set in ${ENV_FILE}." >&2
        exit 1
    fi
done

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <file.sql | directory/>" >&2
    exit 1
fi

TARGET="$1"

run_sql() {
    local file="$1"
    echo "==> Executing: ${file}"
    SNOWSQL_PWD="${SNOWFLAKE_PASSWORD}" snowsql \
        --accountname "${SNOWFLAKE_ACCOUNT}" \
        --username "${SNOWFLAKE_USER}" \
        --rolename "${SNOWFLAKE_ROLE}" \
        --warehouse "${SNOWFLAKE_WAREHOUSE}" \
        --filename "${file}" \
        --option friendly=false \
        --option header=false \
        --option timing=true
}

if [[ -d "${TARGET}" ]]; then
    for sql_file in "${TARGET}"/*.sql; do
        [[ -f "${sql_file}" ]] || continue
        run_sql "${sql_file}"
    done
elif [[ -f "${TARGET}" ]]; then
    run_sql "${TARGET}"
else
    echo "Error: ${TARGET} is not a valid file or directory." >&2
    exit 1
fi

echo "Done."
