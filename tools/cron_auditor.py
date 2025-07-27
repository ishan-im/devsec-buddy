import subprocess
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("reports/cron_audit_log.txt")


def get_cron_jobs(user=None):
    """
    Retrieves the crontab entries for a given user or the current user.
    Returns a list of active cron job lines.
    """
    try:
        if user:
            result = subprocess.run(
                ["crontab", "-l", "-u", user], capture_output=True, text=True
            )
        else:
            result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)

        if result.returncode != 0:
            return []

        # Filter out comments and empty lines
        cron_jobs = [
            line
            for line in result.stdout.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        return cron_jobs

    except Exception as e:
        print(f"[ERROR] Failed to read crontab: {e}")
        return []


def log_cron_jobs(jobs):
    """
    Logs the cron jobs with a timestamp to a file.
    """
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"\n=== CRON AUDIT @ {datetime.now()} ===\n")
        if jobs:
            for job in jobs:
                f.write(job + "\n")
        else:
            f.write("No active cron jobs found.\n")


def audit_cron_jobs(user=None):
    """
    Main function to audit and log cron jobs.
    """
    jobs = get_cron_jobs(user)
    log_cron_jobs(jobs)
    print(f"[INFO] Cron jobs logged ({len(jobs)} entries)")


# For standalone execution and testing
if __name__ == "__main__":
    audit_cron_jobs()
