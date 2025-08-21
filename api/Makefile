# Makefile for Dockerized fastapi

# Define variables for the image name and tag
IMAGE_NAME := fastapi

build:
	@echo "Building Docker image: $(IMAGE_NAME)"
	docker build -t $(IMAGE_NAME) .

run:
	@echo "Running Docker container..."
	docker run --rm -p 8000:8000 $(IMAGE_NAME)

clean:
	@echo "Removing Docker image: $(IMAGE_NAME)"
	docker rmi $(IMAGE_NAME) || true