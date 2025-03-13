import logging
import os
from dataclasses import dataclass

import requests

AUTORIZADOR_HOST = os.environ.get("AUTORIZADOR_HOST")
AUTORIZADOR_PUERTO = os.environ.get("AUTORIZADOR_PUERTO")


@dataclass()
class ClienteAutorizador:
    token: str

    @property
    def base_url(self):
        return f"http://{AUTORIZADOR_HOST}:{AUTORIZADOR_PUERTO}"

    def autorizar(self) -> bool:
        response = requests.post(
            f"{self.base_url}/autorizar", json={"token": self.token}, verify=False
        )

        if response.status_code != 200:
            logging.error(
                f"Error de autorizacion: {response.status_code=} -> {response.text=}"
            )
            return False

        return True
