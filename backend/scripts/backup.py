import subprocess
import os
import boto3
from datetime import datetime
import logging
from ..config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_db_backup():
    """Create a PostgreSQL database backup."""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"backup_{timestamp}.sql"
        
        # Parse database URL
        db_url = settings.DATABASE_URL
        db_parts = db_url.replace("postgresql://", "").split("@")
        auth = db_parts[0].split(":")
        host_port_db = db_parts[1].split("/")
        host_port = host_port_db[0].split(":")
        
        # Set environment variables for pg_dump
        env = os.environ.copy()
        env["PGPASSWORD"] = auth[1]
        
        # Create backup
        cmd = [
            "pg_dump",
            "-h", host_port[0],
            "-p", host_port[1] if len(host_port) > 1 else "5432",
            "-U", auth[0],
            "-d", host_port_db[1],
            "-F", "c",  # Custom format
            "-f", backup_file,
        ]
        
        subprocess.run(cmd, env=env, check=True)
        logger.info(f"Database backup created: {backup_file}")
        return backup_file
    
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to create database backup: {e}")
        raise

def upload_to_s3(file_path: str):
    """Upload backup file to S3."""
    try:
        if not all([
            settings.AWS_ACCESS_KEY_ID,
            settings.AWS_SECRET_ACCESS_KEY,
            settings.AWS_BUCKET_NAME
        ]):
            logger.error("AWS credentials not configured")
            return
        
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        
        # Upload to S3
        bucket = settings.AWS_BUCKET_NAME
        s3_path = f"backups/{os.path.basename(file_path)}"
        
        s3.upload_file(file_path, bucket, s3_path)
        logger.info(f"Backup uploaded to S3: {s3_path}")
        
        # Delete local backup file
        os.remove(file_path)
        logger.info(f"Local backup file deleted: {file_path}")
    
    except Exception as e:
        logger.error(f"Failed to upload backup to S3: {e}")
        raise

def main():
    """Main backup routine."""
    try:
        backup_file = create_db_backup()
        upload_to_s3(backup_file)
        logger.info("Backup process completed successfully")
    except Exception as e:
        logger.error(f"Backup process failed: {e}")
        raise

if __name__ == "__main__":
    main() 