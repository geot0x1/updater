import socket
import threading
import uuid
import struct
import os
import hashlib
from datetime import datetime

TCP_HOST = "0.0.0.0"
TCP_PORT = 9090
CHUNK_SIZE = 4096

FIRMWARE_DIR = os.path.join(os.path.dirname(__file__), '..', 'firmware_files')
METADATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'firmware_metadata.json')

# Shared state (thread-safe)
current_downloads = {}
downloads_lock = threading.Lock()
metadata_lock = threading.Lock()

def now_iso():
    return datetime.utcnow().isoformat() + "Z"

def handle_client(conn, addr):
    ip = addr[0]
    connection_id = f"{ip}-{uuid.uuid4().hex[:8]}"
    print(f"[TCP] Connected: {connection_id}")
    try:
        conn.send(b"Hello TCP Client!\n")
    finally:
        conn.close()
        print(f"[TCP] Disconnected: {connection_id}")

def tcp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_HOST, TCP_PORT))
    s.listen(5)
    print(f"[TCP] Listening on {TCP_HOST}:{TCP_PORT}")
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()
