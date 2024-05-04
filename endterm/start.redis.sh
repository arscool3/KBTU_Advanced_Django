#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

docker run -d --name redis -p 6379:6379 redis/redis-stack-server:latest
