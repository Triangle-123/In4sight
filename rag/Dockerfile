FROM python:3.10-slim

WORKDIR /rag

ARG GITLAB_TOKEN
ARG PROJECT_ID

COPY requirements.txt .

RUN pip install -r requirements.txt --index-url https://__token__:${GITLAB_TOKEN}@lab.ssafy.com/api/v4/projects/${PROJECT_ID}/packages/pypi/simple

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
