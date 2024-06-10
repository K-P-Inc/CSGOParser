#!/bin/bash

# Function to get the service name by image name
get_service_by_image() {
  local image_name=$1
  local service_name=$(yq e '.services[] | select(.image == "'$image_name'") | key' docker-compose.yml)
  echo $service_name
}

# Check if yq is installed
if ! command -v yq &> /dev/null; then
  echo "yq is required but not installed. Please install yq to proceed."
  exit 1
fi

# Image name passed as argument
IMAGE_NAME=$1

if [ -z "$IMAGE_NAME" ]; then
  echo "Usage: $0 <image_name>"
  exit 1
fi

# Get service name from image name
SERVICE_NAME=$(get_service_by_image $IMAGE_NAME)

if [ -z "$SERVICE_NAME" ]; then
  echo "No service found with image name: $IMAGE_NAME"
  exit 1
fi

# Build the service
docker-compose build $SERVICE_NAME --no-cache
