#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


alembic upgrade head
chmod +x journal/consumer.py
python -m journal.consumer