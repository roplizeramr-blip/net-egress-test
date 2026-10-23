FROM python:3.12-alpine

WORKDIR /app
COPY server.py /app/server.py

EXPOSE 3000
CMD ["python3", "/app/server.py"]
