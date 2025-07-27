import socket
import yaml
import os

def scan_ports(ip, ports):
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
    return open_ports

def main():
    config_path = "port_scanner_config.yaml"
    if not os.path.exists(config_path):
        print(f"Config file {config_path} not found.")
        return

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    ip = config["ip"]
    ports = config["ports"]

    open_ports = scan_ports(ip, ports)

    with open("open_ports.txt", "w") as f:
        for port in open_ports:
            f.write(f"{port}\n")
