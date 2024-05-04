#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

postgres_is_not_ready() {
python << END
import os
import psycopg2
import sys

try:
    psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        port=os.environ["POSTGRES_PORT"],
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"]
    )
except psycopg2.OperationalError as e:
    print(e)
    sys.exit(-1)

sys.exit(0)
END
}

until postgres_is_not_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

alembic upgrade head

uvicorn main:app --reload --host 0.0.0.0