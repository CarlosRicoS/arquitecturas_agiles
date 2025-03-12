FROM python:3.9
WORKDIR /app
COPY consumer.py /app/
RUN pip install flask pika
CMD ["python", "consumer.py"]
