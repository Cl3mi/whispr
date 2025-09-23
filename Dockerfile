FROM python:3.10-slim

WORKDIR /whisper

# System deps
RUN apt-get update && apt-get install -y git ffmpeg && rm -rf /var/lib/apt/lists/*

# Install torch with CUDA support
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install --no-cache-dir "git+https://github.com/openai/whisper.git"
RUN pip install --no-cache-dir requests python-dotenv

# Copy everything
COPY . .

CMD ["python3", "transcribe.py"]
