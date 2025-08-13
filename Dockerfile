# Use a minimal Ubuntu 22.04 base image
FROM ubuntu:22.04

# Set DEBIAN_FRONTEND to noninteractive to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install only the necessary packages
# --no-install-recommends prevents installation of optional packages
# Clean up apt cache to reduce image size
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc g++ python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user 'sandboxuser' with user ID 1000 and create its home directory
RUN useradd -m -u 1000 -s /bin/bash sandboxuser

# Switch to the non-root user
USER sandboxuser

# Set the working directory for the user
WORKDIR /sandbox/temp