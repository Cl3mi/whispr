@echo off
SET FLAG=%1

REM ----------------------
REM Help
REM ----------------------
IF "%FLAG%"=="-h" (
    GOTO :help
)
IF "%FLAG%"=="--help" (
    GOTO :help
)
GOTO :main

:help
echo Usage: run_whispr.bat [OPTION]
echo.
echo This Command converts mp4 to audio, creates a transcript using whisper and sends the output to either open-router or openai API to create a summary. Please check the README for further instructions
echo.
echo Options:
echo   --only-transcript   Convert video to audio and transcribe only (skip summary).
echo   -h, --help          Show this help message.
exit /b 0

:main
REM ----------------------
REM 1. Build the Docker image
REM ----------------------
echo 🛠️  Building Docker image 'whispr'...
docker build -t whispr .

REM ----------------------
REM 2. Run the container
REM ----------------------
echo 🚀 Running Docker container 'whispr'...
docker run --gpus all --rm -it ^
    -v "%cd%\video:/whisper/video" ^
    -v "%cd%\audio:/whisper/audio" ^
    -v "%cd%\transcripts:/whisper/transcripts" ^
    -v "%cd%\summaries:/whisper/summaries" ^
    -v "%cd%\.env:/whisper/.env" ^
    whispr python3 transcribe.py %FLAG%
