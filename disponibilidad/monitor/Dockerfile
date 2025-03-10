FROM python:3.12

WORKDIR /app

COPY monitor/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY monitor/__main__.py .

COPY ../servicios ./servicios/

COPY ../monitor/ ./monitor/

CMD [ "python", "/app/__main__.py" ]


