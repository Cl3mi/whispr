#!/bin/bash
# Make sure to give execute permissions: chmod +x run_whispr.sh

FLAG="$1"

# ----------------------
# Help
# ----------------------
if [[ "$FLAG" == "-h" || "$FLAG" == "--help" ]]; then
    echo "Usage: ./run_whispr.sh [OPTION]"
    echo
    echo "This Command converts mp4 to audio, creates a transcript using whisper and sends the output to either open-router or openai API to create a summary. Please check the README for further instructions"
    echo
    echo "Options:"
    echo "  --only-transcript   Convert video to audio and transcribe only (skip summary)."
    echo "  -h, --help          Show this help message."
    exit 0
fi

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
    whispr python3 transcribe.py $FLAG
