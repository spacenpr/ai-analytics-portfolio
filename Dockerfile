FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY advanced_ml_reports/best_model_v2.pkl ./advanced_ml_reports/
COPY model_api.py .
COPY telegram_bot_api.py .

EXPOSE 8000

CMD ["python", "model_api.py"]