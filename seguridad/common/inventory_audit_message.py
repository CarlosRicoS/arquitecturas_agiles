import hashlib
import json
import subprocess


class Inventory_Audit_Message:
    def __init__(self, detail, event_type, uuid, timestamp, host_ip):
        self.detail = detail
        self.event_type = event_type
        self.uuid = uuid
        self.timestamp = timestamp
        self.host_ip = host_ip

    def generar_hash(self, mensaje):
        return hashlib.sha256(json.dumps(mensaje).encode("utf-8")).hexdigest()

    def get_message(self):
        message = {
            "detail": self.detail,
            "event_type": self.event_type,
            "uuid": self.uuid,
            "timestamp": self.timestamp,
            "host_ip": self.host_ip,
        }
        return json.dumps({"check_sum": self.generar_hash(message), "message": message})

    def retrieve_host_ip(self):
        container_ip = subprocess.getoutput("hostname -I").strip()
        print("Container IP Address:", container_ip)
        return container_ip
