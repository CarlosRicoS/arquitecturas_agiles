FROM python:3.9
WORKDIR /app
COPY app.py /app/
RUN pip install flask pika
CMD ["python", "app.py"]
