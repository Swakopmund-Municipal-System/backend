#!/bin/bash
python init_db.py
uvicorn main:app --host 0.0.0.0 --port 8002 --reload