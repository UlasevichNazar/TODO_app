#!/bin/bash

uvicorn app.main:init_app --host ${FASTAPI_HOST} --port ${FASTAPI_PORT} --reload
