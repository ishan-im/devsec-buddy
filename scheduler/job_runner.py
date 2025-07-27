# scheduler/job_runner.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import time
import logging

# Import tool functions
from tools.port_scanner import run_port_scan
from tools.file_integrity import check_file_integrity
from tools.cron_auditor import audit_cron_jobs
from tools.system_monitor import monitor_system

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def schedule_jobs():
    scheduler = BackgroundScheduler()

    # Port Scan every 30 minutes
    scheduler.add_job(
        run_port_scan,
        IntervalTrigger(minutes=30),
        name="Port Scan",
        id="port_scan",
        replace_existing=True,
    )

    # File integrity check every 1 hour
    scheduler.add_job(
        check_file_integrity,
        IntervalTrigger(hours=1),
        name="File Integrity Check",
        id="file_integrity",
        replace_existing=True,
    )

    # Cron audit every 2 hours
    scheduler.add_job(
        audit_cron_jobs,
        IntervalTrigger(hours=2),
        name="Cron Auditor",
        id="cron_audit",
        replace_existing=True,
    )

    # System monitor every 5 minutes
    scheduler.add_job(
        monitor_system,
        IntervalTrigger(minutes=5),
        name="System Monitor",
        id="system_monitor",
        replace_existing=True,
    )

    scheduler.start()
    logging.info("All jobs scheduled. Press Ctrl+C to exit.")

    try:
        while True:
            time.sleep(1)  # Keep main thread alive
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logging.info("Scheduler stopped.")
