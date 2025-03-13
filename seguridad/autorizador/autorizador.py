import logging
import os
from typing import Any

from fastapi import FastAPI, HTTPException
from jwt import InvalidSignatureError, decode
from pydantic import BaseModel

PERMISOS = {
    "inventario_write": {"POST": ["/productos"], "DELETE": ["/productos/<nombre>"]},
    "inventario_read": {"GET": ["/productos"]},
}
PRE_SHARED_KEY = os.getenv("PRE_SHARED_KEY", "")
PUERTO = int(os.getenv("AUTORIZADOR_PUERTO", "8090"))

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


def decodificar_token(solicitud: SolicitudAutorizacion) -> Any:
    try:
        decoded_token = decode(
            solicitud.token, key=PRE_SHARED_KEY, algorithms=["HS256"]
        )
    except InvalidSignatureError:
        raise
    return decoded_token


def autorizar_usuario(solicitud: SolicitudAutorizacion) -> bool:
    decoded_token = decodificar_token(solicitud)
    usuario = decoded_token.get("usuario")
    permiso = decoded_token.get("permiso")
    autorizado = all(
        [
            permiso in PERMISOS,
            solicitud.method in PERMISOS.get(permiso, {}),
            solicitud.path in PERMISOS.get(permiso, {}).get(solicitud.method, []),
        ]
    )
    logging.debug(
        f"[Autorizador]: {usuario=} {permiso=} {solicitud.method=} {solicitud.path=} -> {autorizado=}"
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PUERTO)
