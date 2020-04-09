#!/bin/bash
set -e

python3 -m graphvl -t
uvicorn graphvl.main:app
