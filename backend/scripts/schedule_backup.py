import schedule
import time
import logging
from datetime import datetime
from .backup import main as backup_main

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def job():
    """Run backup job."""
    logger.info(f"Starting scheduled backup at {datetime.now()}")
    try:
        backup_main()
        logger.info("Scheduled backup completed successfully")
    except Exception as e:
        logger.error(f"Scheduled backup failed: {e}")

def main():
    """Schedule and run backup jobs."""
    # Schedule daily backup at 2 AM
    schedule.every().day.at("02:00").do(job)
    
    # Schedule weekly backup on Sunday at 3 AM
    schedule.every().sunday.at("03:00").do(job)
    
    logger.info("Backup scheduler started")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main() 