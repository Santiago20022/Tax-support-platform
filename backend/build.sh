#!/usr/bin/env bash
set -e
pip install -e .
alembic upgrade head
python3 -m app.seeds.run_seeds
