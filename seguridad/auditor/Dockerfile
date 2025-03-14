FROM python:3.12

WORKDIR /app

COPY ./seguridad/auditor/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

COPY ./disponibilidad/servicios ./disponibilidad/servicios/

COPY ./seguridad/auditor/ .

COPY ./setup.py .

RUN pip install -e .

CMD [ "python", "auditor.py" ]