import os
import glob
import subprocess
import whisper
import torch
import requests
from dotenv import load_dotenv

# ----------------------
# Choose service: "openai" or "open-router"
# ----------------------
SERVICE = "openai"

# ----------------------
# Load environment
# ----------------------
load_dotenv(dotenv_path="/whisper/.env")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print(f"DEBUG: SERVICE = {SERVICE}")
if SERVICE == "open-router":
    print(f"DEBUG: OPENROUTER_API_KEY = {OPENROUTER_API_KEY[:6]}...")
elif SERVICE == "openai":
    print(f"DEBUG: OPENAI_API_KEY = {OPENAI_API_KEY[:6]}...")
else:
    raise ValueError(f"Invalid SERVICE value: {SERVICE}")

# ----------------------
# Paths
# ----------------------
VIDEO_FOLDER = "/whisper/video"
AUDIO_FOLDER = "/whisper/audio"
TRANSCRIPT_FOLDER = "/whisper/transcripts"
SUMMARY_FOLDER = "/whisper/summaries"
PROMPT_FILE = "/whisper/prompt.txt"

os.makedirs(AUDIO_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)
os.makedirs(SUMMARY_FOLDER, exist_ok=True)

# ----------------------
# Whisper model
# ----------------------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Loading Whisper model on {DEVICE}...")
model = whisper.load_model("base", device=DEVICE)

# ----------------------
# Helpers
# ----------------------


def convert_videos_to_mp3():
    video_files = glob.glob(os.path.join(VIDEO_FOLDER, "*.mp4"))
    if not video_files:
        print("⚠️ No .mp4 files found in " + VIDEO_FOLDER)
    for vf in video_files:
        base = os.path.splitext(os.path.basename(vf))[0]
        audio_file = os.path.join(AUDIO_FOLDER, f"{base}.mp3")
        if not os.path.exists(audio_file):
            print(f"🎬 Converting {vf} → {audio_file}")
            subprocess.run(["ffmpeg", "-i", vf, "-vn",
                           "-acodec", "mp3", audio_file], check=True)
        else:
            print(f"ℹ️ Audio already exists: {audio_file}")


def transcribe_audio():
    mp3_files = glob.glob(os.path.join(AUDIO_FOLDER, "*.mp3"))
    if not mp3_files:
        print(f"⚠️ No .mp3 files found in " + AUDIO_FOLDER)
    for af in mp3_files:
        base = os.path.splitext(os.path.basename(af))[0]
        out_file = os.path.join(TRANSCRIPT_FOLDER, f"{base}.txt")
        if not os.path.exists(out_file):
            print(f"🎧 Transcribing {af} on {DEVICE}...")
            result = model.transcribe(af)
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(result["text"])
            print(f"✅ Saved transcript → {out_file}")
        else:
            print(f"ℹ️ Transcript already exists: {out_file}")


def summarize_transcript():
    # Read prompt
    if not os.path.exists(PROMPT_FILE):
        print(f"⚠️ Prompt file {PROMPT_FILE} not found, using empty prompt.")
        custom_prompt = ""
    else:
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            custom_prompt = f.read().strip()
    print(f"DEBUG: prompt content = {custom_prompt[:100]}")

    transcript_files = glob.glob(os.path.join(TRANSCRIPT_FOLDER, "*.txt"))
    if not transcript_files:
        print(f"⚠️ No transcripts found in" +
              TRANSCRIPT_FOLDER + ", skipping summary.")
        return

    for tf in transcript_files:
        base = os.path.splitext(os.path.basename(tf))[0]
        out_file = os.path.join(SUMMARY_FOLDER, f"{base}.txt")
        if os.path.exists(out_file):
            print(f"ℹ️ Summary already exists: {out_file}")
            continue

        with open(tf, "r", encoding="utf-8") as f:
            transcript = f.read()

        payload = {
            "model": "gpt-5",
            "messages": [
                {"role": "system", "content": custom_prompt},
                {"role": "user", "content": transcript}
            ]
        }

        if SERVICE == "open-router":
            key = OPENROUTER_API_KEY
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            }
        elif SERVICE == "openai":
            key = OPENAI_API_KEY
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            }
        else:
            raise ValueError(f"Invalid SERVICE value: {SERVICE}")

        print(f"📤 Sending transcript {tf} to {SERVICE}...")
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=500)
            # Debug raw response if needed
            print("DEBUG: raw response:", r.text[:500])
            if r.text.strip().startswith("<!DOCTYPE html>"):
                raise ValueError(
                    f"{SERVICE} returned HTML, likely invalid model name or endpoint.")
            r.raise_for_status()
            summary = r.json()["choices"][0]["message"]["content"]
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(summary)
            print(f"✅ Saved summary → {out_file}")
        except Exception as e:
            print(f"❌ Failed to summarize {tf}: {e}")


# ----------------------
# Main pipeline
# ----------------------
if __name__ == "__main__":
    print("Looking for videos in:", VIDEO_FOLDER)
    print("Found:", os.listdir(VIDEO_FOLDER))

    convert_videos_to_mp3()
    print("Looking for mp3 audio in:", AUDIO_FOLDER)
    print("Found:", os.listdir(AUDIO_FOLDER))

    transcribe_audio()
    print("Looking for transcripts in:", TRANSCRIPT_FOLDER)
    print("Found:", os.listdir(TRANSCRIPT_FOLDER))

    summarize_transcript()
    print("Looking for summaries in:", SUMMARY_FOLDER)
    print("Found:", os.listdir(SUMMARY_FOLDER))
