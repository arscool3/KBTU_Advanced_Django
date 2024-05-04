#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000