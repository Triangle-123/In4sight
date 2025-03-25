"""
FastAPI 서버를 올리기 위한 main.py
"""

from fastapi import FastAPI

from app.lifespan import lifespan

app = FastAPI(lifespan=lifespan)
