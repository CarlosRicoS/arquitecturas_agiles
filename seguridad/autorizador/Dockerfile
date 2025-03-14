FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt update

RUN apt -y install libsasl2-dev python-dev-is-python3 libldap2-dev libssl-dev

COPY . .

EXPOSE ${AUTORIZADOR_PUERTO}