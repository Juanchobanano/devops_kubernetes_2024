#!/usr/bin/env bash
set -e

# Ensure the required environment variables are set
if [ -z "$BACKUP_BUCKET" ] || [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_PASSWORD" ] || [ -z "$DATABASE_HOST" ] || [ -z "$DATABASE_PORT" ] || [ -z "$POSTGRES_DB" ]; then
  echo "POSTGRES_USER, POSTGRES_PASSWORD, DATABASE_HOST, DATABASE_PORT, and POSTGRES_DB, BACKUP_BUCKET must be set"
  exit 1
fi

# Construct the PostgreSQL URL dynamically using the environment variables
URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DATABASE_HOST}:${DATABASE_PORT}/${POSTGRES_DB}"

# Perform the backup using pg_dump
pg_dump -v $URL > /usr/src/app/backup.sql

# Authenticate with Google Cloud using the mounted service account key
export GOOGLE_APPLICATION_CREDENTIALS="/etc/gcp/key.json"

# Upload the backup to Google Cloud Storage
curl -F 'data=@/usr/src/app/backup.sql' \
     "https://storage.googleapis.com/${BACKUP_BUCKET}/backup-$(date +%Y%m%d%H%M%S).sql"

echo "Backup uploaded to Google Cloud Storage"