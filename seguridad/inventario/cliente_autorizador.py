import logging
import os
from dataclasses import dataclass

import requests

AUTORIZADOR_URL = os.environ.get("AUTORIZADOR_URL")


@dataclass()
class ClienteAutorizador:
    token: str

    def autorizar(self, method: str, path: str) -> str | None:
        payload = {
            "token": self.token,
            "method": method,
            "path": path,
        }

        response = requests.post(
            f"{AUTORIZADOR_URL}/autorizar", json=payload, verify=False
        )

        if response.status_code != 200:
            logging.error(
                f"Error de autorizacion: {response.status_code=} -> {response.text=}"
            )
            return None

        return response.json()["user"]
