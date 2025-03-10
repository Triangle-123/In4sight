"""
FASTAPI APP 메인 파일
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """
    루트 경로 호출 시 반환되는 메시지
    """
    return {"message": "Hello World"}
