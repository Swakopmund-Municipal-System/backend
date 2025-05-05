#!/bin/bash
python -c "import asyncio; from init_db import create_tables; asyncio.run(create_tables())"
uvicorn main:app --host 0.0.0.0 --port 8002