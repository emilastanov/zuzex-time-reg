FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV ENV=production

CMD ["python3", "main.py"]