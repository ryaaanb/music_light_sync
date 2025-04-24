FROM python:3.11-slim

WORKDIR /app

COPY run.py .
COPY web/ ./web/

RUN apt-get update && apt-get install -y portaudio19-dev && \
    pip install flask requests sounddevice numpy

CMD ["python", "run.py"]
