#!/bin/bash

# Define directories for your services
KAFKA_SETUP_DIR="Kafka setup"
SPARK_SETUP_DIR="spark_setup"
POSTGRES_SETUP_DIR="Postgresql_setup"

# Function to bring down services in a directory
bring_down_services() {
    local dir="$1"
    if [ -d "$dir" ]; then
        echo "Navigating to $dir directory..."
        cd "$dir" || exit
        echo "Bringing down services with docker-compose..."
        docker compose down
        if [ $? -eq 0 ]; then
            echo "Successfully brought down services in $dir."
        else
            echo "Failed to bring down services in $dir."
        fi
        cd .. || exit
    else
        echo "Directory $dir does not exist."
    fi
}

# Bring down services for each setup
bring_down_services "$KAFKA_SETUP_DIR"
bring_down_services "$SPARK_SETUP_DIR"
bring_down_services "$POSTGRES_SETUP_DIR"

echo "All services have been brought down."