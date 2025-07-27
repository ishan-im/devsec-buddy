# tools/port_scanner.py

import socket
import yaml
import json
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path("configs/monitored_ports.yaml")
REPORT_PATH = Path("reports/scan_results.json")


def load_scan_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError("Missing monitored_ports.yaml")
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def is_port_open(ip, port, timeout=1):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def run_port_scan():
    config = load_scan_config()
    ip = config.get("target_ip", "127.0.0.1")
    ports = config.get("ports", list(range(1, 1025)))

    results = {"target": ip, "timestamp": datetime.now().isoformat(), "open_ports": []}

    for port in ports:
        if is_port_open(ip, port):
            results["open_ports"].append(port)

    with open(REPORT_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"[✓] Scan complete. Open ports: {results['open_ports']}")
