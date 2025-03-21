# Python 3.11 이미지를 기반으로 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app/

# Jenkins 워크스페이스의 .venv를 컨테이너로 복사
COPY .venv /app/.venv
COPY . .
COPY .env .

ENV PATH="/app/.venv/bin:$PATH"

# 포트 설정
EXPOSE 8000

# FastAPI 서버 실행 (가상환경의 Python 사용)
CMD [".venv/bin/python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]