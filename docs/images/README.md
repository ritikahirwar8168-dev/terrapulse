# TerraPulse Interface Previews & Screenshot Guidelines

This directory contains visual assets and interface screenshots for **TerraPulse**.

## Recommended Screenshot Catalog

| Filename | Description | Viewport / Section |
| :--- | :--- | :--- |
| `dashboard.png` | Main interactive interface showing environmental sliders, mission selectors, and trail presets. | Full desktop view (`1280x800` or higher) |
| `analysis_result.png` | Generated results showing the Grass Score gauge, TabPFN trail physics prediction, and frost risk card. | Results card section |
| `audio_briefing.png` | Spoken outdoor field briefing quote, micro-quest challenge box, and audio player controls. | Audio player & quest section |
| `sentry_waterfall.png` | Sentry Agent Tracing waterfall view displaying live execution spans (`tabpfn.inference`, `gemma.reasoning`, `elevenlabs.tts_stream`). | Latency waterfall section |

## How to Capture Screenshots

1. Launch the local application:
   ```bash
   uvicorn app:app --port 8000
   ```
2. Open `http://localhost:8000` in your browser.
3. Select an activity preset (e.g., **Pine Ridge Trail** or **Misty Creek Hollow**).
4. Click **"Synthesize Briefing & Touch Grass"** to populate predictions, briefings, and waterfall spans.
5. Capture clean screenshots using your system screenshot tool or browser developer tools (Ctrl+Shift+P > "Capture screenshot").
6. Save the PNG files into `docs/images/` using the exact filenames listed above.
