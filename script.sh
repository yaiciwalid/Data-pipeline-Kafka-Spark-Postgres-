#!/bin/bash

# Define the network name
NETWORK_NAME="spark-kafka"

# Check if the Docker network exists
if docker network ls | grep -q "$NETWORK_NAME"; then
    echo "Network '$NETWORK_NAME' already exists."
else
    echo "Network '$NETWORK_NAME' does not exist. Creating it now..."
    docker network create "$NETWORK_NAME"
    
    if [ $? -eq 0 ]; then
        echo "Network '$NETWORK_NAME' successfully created."
    else
        echo "Failed to create network '$NETWORK_NAME'."
        exit 1
    fi
fi


# Go to the Kafka_setup folder
KAFKA_SETUP_DIR="Kafka setup"
if [ -d "$KAFKA_SETUP_DIR" ]; then
    echo "Navigating to the $KAFKA_SETUP_DIR directory."
    cd "$KAFKA_SETUP_DIR"
    
    # Run docker-compose up
    echo "Running docker-compose up..."
    docker compose up -d

    if [ $? -eq 0 ]; then
        echo "docker-compose up executed successfully."
    else
        echo "Failed to run docker-compose up."
        exit 1
    fi
else
    echo "Directory $KAFKA_SETUP_DIR does not exist."
    exit 1
fi

cd ".."
# Go to the postgre folder and run docker-compose up
POSTGRE_DIR="Postgresql_setup"
if [ -d "$POSTGRE_DIR" ]; then
    echo "Navigating to the $POSTGRE_DIR directory."
    cd "$POSTGRE_DIR"
    
    # Run docker-compose up in postgre
    echo "Running docker-compose up in postgre..."
    docker compose up -d

    if [ $? -eq 0 ]; then
        echo "docker-compose up in postgre executed successfully."
    else
        echo "Failed to run docker-compose up in postgre."
        exit 1
    fi
else
    echo "Directory $POSTGRE_DIR does not exist."
    exit 1
fi

# Go back to the parent directory
cd ..

# Navigate to the spark_setup folder and run docker-compose up
SPARK_SETUP_DIR="spark_setup"
if [ -d "$SPARK_SETUP_DIR" ]; then
    echo "Navigating to the $SPARK_SETUP_DIR directory."
    cd "$SPARK_SETUP_DIR"
    
    # Run docker-compose up in spark_setup
    echo "Running docker-compose up in spark_setup..."
    docker compose up -d

    if [ $? -eq 0 ]; then
        echo "docker compose up in spark_setup executed successfully."
    else
        echo "Failed to run docker-compose up in spark_setup."
        exit 1
    fi
else
    echo "Directory $SPARK_SETUP_DIR does not exist."
    exit 1
fi

# Execute spark-submit in the spark-master container if everything is successful
SPARK_MASTER_CONTAINER="spark-master"

echo "Checking the container '$SPARK_MASTER_CONTAINER'..."

# Check if the spark-master container is running
if docker ps | grep -q "$SPARK_MASTER_CONTAINER"; then
    echo "The container '$SPARK_MASTER_CONTAINER' is running. Executing spark-submit..."
    
    # Execute spark-submit in the spark-master container
    docker compose exec -d "$SPARK_MASTER_CONTAINER" spark-submit \
      --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.postgresql:postgresql:42.2.18 \
      /opt/spark-apps/spark_consumer.py

    if [ $? -eq 0 ]; then
        echo "The spark-submit command executed successfully in the container $SPARK_MASTER_CONTAINER."
    else
        echo "Failed to execute the spark-submit command in the container $SPARK_MASTER_CONTAINER."
        exit 1
    fi
else
    echo "The container '$SPARK_MASTER_CONTAINER' is not running."
    exit 1
fi
