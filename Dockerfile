FROM python:3.11-slim

WORKDIR /app

# 의존성 먼저 복사 (레이어 캐시 활용)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 복사
COPY . .

# HuggingFace Spaces는 포트 7860 사용
EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
