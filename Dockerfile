FROM python:3.12
RUN pip install pika
WORKDIR /app
COPY __main__.py .
COPY servicios/ ./servicios/
COPY monitor/ ./monitor/

ENTRYPOINT [ "python", "/app/__main__.py" ]


