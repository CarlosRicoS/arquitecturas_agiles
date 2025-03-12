FROM python:3.12

WORKDIR /app

COPY ./seguridad/deteccion_intrusos/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

COPY ./disponibilidad/servicios ./disponibilidad/servicios/

COPY ./seguridad/deteccion_intrusos/ ./deteccion_intrusos/

COPY ./setup.py .

RUN pip install -e .

CMD [ "python", "/app/deteccion_intrusos/__main__.py" ]


