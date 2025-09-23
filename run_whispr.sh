#!/bin/bash
# Make sure to give execute permissions: chmod +x run_whispr.sh

# ----------------------
# 1. Build the Docker image
# ----------------------
echo "🛠️  Building Docker image 'whispr'..."
docker build -t whispr .

# ----------------------
# 2. Run the container
# ----------------------
echo "🚀 Running Docker container 'whispr'..."
docker run --gpus all --rm -it \
    -v "$(pwd)/video:/whisper/video" \
    -v "$(pwd)/audio:/whisper/audio" \
    -v "$(pwd)/transcripts:/whisper/transcripts" \
    -v "$(pwd)/summaries:/whisper/summaries" \
    -v "$(pwd)/.env:/whisper/.env" \
    whispr
