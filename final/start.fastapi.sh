#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

alembic upgrade head
chmod 777 shared_storage
chmod 777 shared_storage/reports
chmod -R 777 shared_storage/reports
uvicorn main:app --reload --host 0.0.0.0 --port 8000