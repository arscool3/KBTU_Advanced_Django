#!/bin/bash

python bot.py & python consumer.py & uvicorn main:app --reload --host 0.0.0.0 --port 8000