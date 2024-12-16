FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY app/ /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "service.py"]
