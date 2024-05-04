#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


alembic upgrade head
chmod +x app/kafka/consumer.py
python -m app.kafka.consumer