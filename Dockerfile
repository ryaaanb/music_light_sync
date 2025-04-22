FROM python:3.11-slim

WORKDIR /app

COPY run.py .
COPY web/ ./web/

RUN pip install flask requests werkzeug

CMD ["python", "run.py"]
