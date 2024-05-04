#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

dramatiq --watch . app.dramatiq_job.main
