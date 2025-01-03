# Use an official PostgreSQL client as the base image
FROM postgres:alpine

# Install curl (optional, if you plan to send the dump somewhere)
RUN apk add --no-cache curl

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the backup script into the container
COPY ./src/backup.sh /usr/src/app/backup.sh

# Make sure the backup script is executable
RUN chmod +x /usr/src/app/backup.sh

# Define the entrypoint to run the script
ENTRYPOINT ["/usr/src/app/backup.sh"]
