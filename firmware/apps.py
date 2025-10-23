from django.apps import AppConfig
import threading

class FirmwareConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'firmware'

    def ready(self):
        # Start TCP server in background
        from .tcp_server import tcp_server
        threading.Thread(target=tcp_server, daemon=True).start()
