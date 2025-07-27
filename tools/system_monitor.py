# tools/system_monitor.py

import psutil
import json
from datetime import datetime
from pathlib import Path

REPORT_PATH = Path("reports/system_metrics.json")


def collect_system_metrics():
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": {
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "used_percent": psutil.virtual_memory().percent,
        },
        "disk": {
            "total": psutil.disk_usage("/").total,
            "used": psutil.disk_usage("/").used,
            "free": psutil.disk_usage("/").free,
            "used_percent": psutil.disk_usage("/").percent,
        },
    }


def write_metrics_report():
    metrics = collect_system_metrics()
    with open(REPORT_PATH, "a") as f:
        json.dump(metrics, f)
        f.write("\n")
    print("[✓] System metrics recorded.")


if __name__ == "__main__":
    write_metrics_report()
