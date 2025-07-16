#!/bin/bash

# Build the Docker image locally for testing
# This sets the BUILD_FROM argument that Home Assistant would normally provide

echo "Building national-rail-departure-board Docker image..."

# Use a standard Home Assistant base image for local builds
docker build \
  --build-arg BUILD_FROM=ghcr.io/home-assistant/aarch64-base:latest \
  -t national-rail-departure-board:local \
  .

echo "Build complete!"
echo "To run the container locally:"
echo "docker run -p 8124:8124 national-rail-departure-board:local" 