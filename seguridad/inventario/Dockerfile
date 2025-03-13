FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install flask pika requests

CMD ["python", "app.py"]
