FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY app/ /app/

RUN pip install --no-cache-dir flask sqlalchemy psycopg2-binary requests lxml

EXPOSE 5000

CMD ["python", "service.py"]
