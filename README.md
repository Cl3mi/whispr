# whispr

**Transcribe → Summarize → Understand**  
Whispr ist eine Dockerized Pipeline, die Videos automatisch in Text und Zusammenfassungen umwandelt.  
Sie nutzt [OpenAI Whisper](https://github.com/openai/whisper) für die Transkription und LLMs (OpenAI / OpenRouter) für die Zusammenfassung.

---

## ✨ Features

- 🎬 **Video → Audio**: `.mp4` → `.mp3` mit `ffmpeg`
- 🎧 **Audio → Transcript**: Transkription mit Whisper (GPU-beschleunigt, falls verfügbar)
- 📝 **Transcript → Summary**: Automatische Zusammenfassungen mit OpenAI, OpenRouter oder LM Studio
- 🐳 **Dockerized**: Einfache Nutzung mit GPU-Support (zurzeit nur von OP mit NVIDIA GPU's getestet)
- ⚡ **Flags & Workflows**: Flexible Ausführung mit `--only-transcript` oder Standard-Workflow

---

## 📂 Projektstruktur

```
.
├── transcribe.py         # Hauptpipeline
├── transcribe_api.py     # Flask API für Uploads
├── run_whispr.sh         # Script für Docker build & run
├── Dockerfile            # Containerdefinition
├── video/                # Inputvideos (.mp4)
├── audio/                # Extrahiertes Audio (.mp3)
├── transcripts/          # Transkripte (.txt)
├── summaries/            # Zusammenfassungen (.txt)
├── prompt.txt            # Optionaler Custom-Prompt
├── .env                  # API Keys
```

---

## ⚡ Quickstart

### 1. Clone & Build
```bash
git clone https://github.com/yourusername/whispr.git
cd whispr
./setup.sh # erstellt benötigte ordner video/, audio/, transcripts/, summaries/
```

👉 Baut das Docker-Image `whispr` und startet den Container mit allen notwendigen Mounts.

---

### 2. Videos hinzufügen
Lege deine `.mp4` Dateien im Ordner `video/` ab.

---

### 3. Environment konfigurieren
Erstelle eine `.env` Datei mit deinen Keys:

```ini
OPENAI_API_KEY=sk-xxxx
OPENROUTER_API_KEY=or-xxxx
```

Wähle den Service in `transcribe.py`:
```python
SERVICE = "openai"       # "openai", "open-router", or "lm-studio"
```

Wähle das gewollte AI Modell in `transcribe.py`:
```python
MODEL_NAME = "gpt-5"       # (By Default its set to an openai API Model)
```

---

### 4. Prompt anpassen
Gegebenenfals prompt.txt nach vorlieben anpassen

---

### 5. Pipeline ausführen
Standard (Video → Audio → Transcript → Summary):
```bash
./run_whispr.sh
```
Nur bis Transkript (keine API-Zusammenfassung):
```bash
./run_whispr.sh --only-transcript
```
Hilfe anzeigen:
```bash
./run_whispr.sh -h
```

Die Pipeline konvertiert automatisch:

1. `.mp4` → `.mp3`
2. `.mp3` → Transkript (`transcripts/`)
3. Transkript → Zusammenfassung (`summaries/`)

---

## 🛠 Dependencies

- Python 3.10
- [PyTorch](https://pytorch.org/) (CUDA falls verfügbar)
- [Whisper](https://github.com/openai/whisper)
- ffmpeg
- requests
- python-dotenv

👉 Alles wird automatisch im Docker-Container installiert.

---

## 📌 Roadmap

- [ ] Mehr Whisper-Modelle (`tiny`, `small`, `medium`, `large`)
- [ ] Leichtere Konfiguration von genutzten AI-Modellen
- [ ] Verbessertes docker-handling
- [ ] Gegebenenfalls automatische Ausführung bei Ablage in Ordner

---

## 📄 License

MIT License — frei nutzbar, veränderbar und teilbar.
