import base64
import hashlib
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from fastapi import FastAPI, HTTPException
from jwt import InvalidSignatureError
from pydantic import BaseModel
from starlette.responses import JSONResponse

PUERTO = int(os.getenv("AUTORIZADOR_PUERTO", "8090"))
AUDIENCE = os.getenv("AUDIENCE", "inventario-test")
ALGORITHM = "RS256"

PERMISOS_INVENTARIO = {
    "inventario_write": {"POST": ["/productos"], "DELETE": ["/productos/<nombre>"]},
    "inventario_read": {"GET": ["/productos"]},
}
PERMISOS_MESSAGE_BROKER = [
    f"{AUDIENCE}.read:*/*/*",
    f"{AUDIENCE}.write:*/*/*",
    f"{AUDIENCE}.configure:*/*/*",
]
USUARIOS_PERMISOS = {
    "detector": PERMISOS_MESSAGE_BROKER,
    "publisher": PERMISOS_MESSAGE_BROKER,
    "auditor": PERMISOS_MESSAGE_BROKER,
    "usuario_legitimo": ["inventario_write", "inventario_read"],
    "usuario_intruso": ["inventario_write"],
}

PRIVATE_KEY_PATH = "config/keys/private.pem"
PUBLIC_KEY_PATH = "config/keys/public.pem"


logging.basicConfig(
    level=logging.DEBUG,
    format="%(name)s|[%(levelname)s]|%(asctime)s|%(message)s",
    handlers=[
        logging.FileHandler("logs/autorizador.log", mode="w"),
        logging.StreamHandler(),
    ],
)
app = FastAPI()


class SolicitudAutorizacion(BaseModel):
    method: str
    path: str
    token: str


class RespuestaAutorizacion(BaseModel):
    token: str


class JWK(BaseModel):
    n: str
    e: str
    kid: str
    kty: str = "RSA"
    alg: str = ALGORITHM


class JWKS(BaseModel):
    keys: list[JWK]


def leer_llave_privada() -> str:
    with open(PRIVATE_KEY_PATH, "r") as private_key_file:
        private_key = private_key_file.read()
    return private_key


def leer_llave_publica() -> RSAPublicKey:
    with open(PUBLIC_KEY_PATH, "rb") as public_key_file:
        public_key: RSAPublicKey = serialization.load_pem_public_key(
            public_key_file.read(), backend=default_backend()
        )
    return public_key


def generar_jwks() -> JWKS:
    public_key = leer_llave_publica()

    public_numbers = public_key.public_numbers()
    n = public_numbers.n
    e = public_numbers.e
    n_bytes = n.to_bytes((n.bit_length() + 7) // 8, "big")
    e_bytes = e.to_bytes((e.bit_length() + 7) // 8, "big")
    n_base64 = base64.urlsafe_b64encode(n_bytes).rstrip(b"=").decode("utf-8")
    e_base64 = base64.urlsafe_b64encode(e_bytes).rstrip(b"=").decode("utf-8")
    kid_input = f"{n_base64}{e_base64}".encode("utf-8")
    kid = (
        base64.urlsafe_b64encode(hashlib.sha256(kid_input).digest())
        .rstrip(b"=")
        .decode("utf-8")
    )
    return JWKS(keys=[JWK(n=n_base64, e=e_base64, kid=kid)])


def generar_token(usuario) -> str:
    private_key = leer_llave_privada()
    permisos = USUARIOS_PERMISOS.get(usuario, [])

    jwks = generar_jwks()
    kid = jwks.keys[0].kid

    headers = {"kid": kid, "alg": ALGORITHM, "typ": "JWT"}

    payload = {
        "sub": usuario,
        "aud": AUDIENCE,
        "iat": datetime.now(),
        "exp": datetime.now() + timedelta(minutes=7200),
        "scope": permisos,
    }
    token = jwt.encode(payload, private_key, algorithm=ALGORITHM, headers=headers)
    return token


def decodificar_token(solicitud: SolicitudAutorizacion) -> Any:
    public_key = leer_llave_publica()
    try:
        decoded_token = jwt.decode(
            solicitud.token, key=public_key, algorithms=[ALGORITHM], audience=AUDIENCE
        )
    except InvalidSignatureError:
        raise
    return decoded_token


def autorizar_usuario(solicitud: SolicitudAutorizacion) -> bool:
    autorizado = False
    decoded_token = decodificar_token(solicitud)
    usuario = decoded_token.get("sub")
    permisos = decoded_token.get("scope")

    for permiso in permisos:
        autorizado = all(
            [
                permiso in PERMISOS_INVENTARIO,
                solicitud.method in PERMISOS_INVENTARIO.get(permiso, {}),
                solicitud.path
                in PERMISOS_INVENTARIO.get(permiso, {}).get(solicitud.method, []),
            ]
        )
        if autorizado:
            break
    logging.debug(
        f"[Autorizador]: {usuario=} {permisos=} {solicitud.method=} {solicitud.path=} -> {autorizado=}"
    )
    return autorizado


@app.post("/autorizar", response_model=RespuestaAutorizacion)
def autorizar(solicitud: SolicitudAutorizacion) -> RespuestaAutorizacion:
    try:
        autorizado = autorizar_usuario(solicitud)
        if not autorizado:
            raise HTTPException(status_code=403, detail="Permission denied")
        return RespuestaAutorizacion(token=solicitud.token)
    except InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/token/{usuario}", response_model=RespuestaAutorizacion)
def token_usuario(usuario: str) -> RespuestaAutorizacion:
    token = generar_token(usuario)
    return RespuestaAutorizacion(token=token)


@app.get("/.well-known/jwks.json", response_model=JWKS)
def jwks() -> JWKS:
    return generar_jwks()


@app.get("/health")
async def health():
    return "ok"


# @app.post("/probar/jwks")
# def probar_jwks(token: str) -> JSONResponse:
#     jwks = generar_jwks()
#
#     key = jwks.keys[0]
#     public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key.__dict__))
#     decoded_payload = jwt.decode(
#         token, public_key, algorithms=["RS256"], audience=AUDIENCE
#     )
#     return JSONResponse(content=decoded_payload)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PUERTO)
