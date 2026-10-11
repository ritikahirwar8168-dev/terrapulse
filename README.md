# 🌿 TerraPulse — Screenless Outdoor & Trail AI Agent

> **Theme: "Touch Grass"** — *Make the screen the shortest part of the experience (< 30 seconds) and get into the wild.*

[![Gemma](https://img.shields.io/badge/Model-Google%20Gemma%202-blue.svg)](https://ai.google.dev/gemma)
[![Prior Labs TabPFN](https://img.shields.io/badge/Foundation-Prior%20Labs%20TabPFN-violet.svg)](https://priorlabs.ai)
[![ElevenLabs](https://img.shields.io/badge/Audio-ElevenLabs%20TTS-amber.svg)](https://elevenlabs.io)
[![Sentry](https://img.shields.io/badge/Observability-Sentry%20Agent%20Tracing-rose.svg)](https://sentry.io)
[![Render](https://img.shields.io/badge/Deploy-Render-teal.svg)](https://render.com)

---

## 🧭 Why Open Innovation Matters for "Touch Grass"

When you are deep on a mountain ridge, inside a national park, or working in a rural garden plot, **cell reception drops to zero**. 

- **Proprietary Cloud APIs Fail Outdoors:** Cloud-reliant proprietary APIs (like OpenAI or Claude) throw network timeouts when you are on a hiking trail or mountain pass.
- **Edge Sovereignty & Zero Latency:** Open-weight models like **Google Gemma 2** and tabular foundation models like **Prior Labs TabPFN** run directly on edge laptops or offline environments.
- **Privacy & Zero Cost:** Microclimate telemetry and location data never leave your device, and there are zero per-token subscriptions to enjoy the natural outdoors.

---

## 🎯 How TerraPulse Works (The 15-Second Flow)

1. **Select Mission & Microclimate (5 seconds):** Pick your trail preset or adjust sliders (temperature, humidity, soil moisture, elevation, canopy cover, hours since rain).
2. **Prior Labs TabPFN (10 milliseconds):** The TabPFN tabular foundation model predicts:
   - **Trail Traction & Safety Condition** (`Prime Dry`, `Muddy & Slippery`, `Frost & Ice Hazard`)
   - **Sub-surface Frost Probability**
   - **Grass Score (0–100%)** measuring outdoor invitingness.
3. **Google Gemma 2 Open-Weight Reasoning:** Gemma synthesizes the TabPFN predictions into:
   - A **15-second Spoken Field Briefing**
   - A hands-on **Micro-Quest** (e.g., *"Find 3 distinct wild fungi varieties on shaded oak trunks"*)
   - A **Sensory Mindfulness Anchor** (e.g., damp petrichor of fallen cedar needles).
4. **ElevenLabs Audio Narration:** Converts the briefing into audio. You hit play, **pocket your phone**, and head outside.
5. **Sentry Agent Waterfall Tracing:** Full execution spans (`tabpfn.inference`, `gemma.reasoning`, `elevenlabs.tts_stream`) are traced with latency metrics.

---

## 🏆 Prize Categories Targeted

| Category | Sponsor | Implementation in TerraPulse |
| :--- | :--- | :--- |
| **Best Use of Gemma** | **Gemma ($200)** | Uses Google's open-weight **Gemma 2** (`gemma-2-9b-it`) for outdoor reasoning and generating screen-free micro-quests. |
| **Best Use of TabPFN** | **Prior Labs ($200)** | Implements **TabPFN** (`tabpfn.TabPFNClassifier`) on tabular environmental data for instant in-context classification without training. |
| **Best Use of Render** | **Render ($200)** | Fully configured with `render.yaml` blueprint for 1-click cloud deployment as an AI runtime. |
| **Best Use of ElevenLabs** | **ElevenLabs ($100)** | Generates lifelike voice narration using ElevenLabs Turbo v2.5 (`JBFqnCBsd6RMkjVDRZzb` voice). |
| **Best Use of Sentry** | **Sentry ($100)** | Uses `sentry-sdk` custom agent tracing to profile each step in the agent waterfall. |

---

## 🚀 Quickstart & Local Execution

### 1. Clone & Install Dependencies
```bash
git clone <repo-url>
cd terrapulse
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)
TerraPulse is designed with robust offline fallbacks so **it works out of the box with zero keys!**
To enable live cloud endpoints, copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Add your optional keys:
- `GEMMA_API_KEY`: Google AI Studio or Ollama endpoint for Gemma 2
- `ELEVENLABS_API_KEY`: ElevenLabs text-to-speech API key
- `SENTRY_DSN`: Sentry project DSN for agent tracing dashboard

### 3. Run Application
```bash
python app.py
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser!

---

## ☁️ Deployment on Render

TerraPulse includes a native `render.yaml` blueprint:
1. Connect this repository to [Render.com](https://render.com).
2. Choose **Blueprint** deployment.
3. Render will automatically build the environment and launch `uvicorn app:app`.

---

## 📸 Sentry Agent Waterfall Trace
TerraPulse visualizes execution performance directly in the UI:
- **`ai.tabpfn.tabular`**: TabPFN in-context tabular prediction (~15ms)
- **`ai.gemma.llm`**: Gemma 2 open-weight reasoning (~120ms)
- **`ai.elevenlabs.tts`**: ElevenLabs audio voice stream (~180ms)

*Put the screen away, breathe the fresh air, and Touch Grass!*
