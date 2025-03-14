FROM python:3.12

WORKDIR /app

COPY ./seguridad/inventario/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

COPY ./disponibilidad/servicios ./disponibilidad/servicios/

COPY ./seguridad/common/ ./seguridad/common/

COPY ./seguridad/inventario/ .

COPY ./setup.py .

RUN pip install -e .

CMD ["python", "app.py"]
