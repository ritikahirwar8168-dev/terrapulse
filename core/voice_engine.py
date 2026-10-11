import os
import time
import base64
from typing import Dict, Any, Optional

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb") # Calm nature narrator

class VoiceEngine:
    """
    ElevenLabs Voice Synthesis Engine for TerraPulse.
    Converts Gemma's screenless nature briefing into natural, high-definition audio narration,
    allowing hikers and gardeners to put their phone in their pocket and explore hands-free.
    """
    def __init__(self):
        self.api_key = ELEVENLABS_API_KEY
        self.voice_id = ELEVENLABS_VOICE_ID

    def synthesize_briefing(self, text: str) -> Dict[str, Any]:
        start_time = time.perf_counter()
        audio_base64 = None
        engine_type = "WebSpeech / Native Browser Audio Fallback"
        character_count = len(text)

        if self.api_key:
            try:
                import requests
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
                headers = {
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                    "xi-api-key": self.api_key
                }
                data = {
                    "text": text,
                    "model_id": "eleven_turbo_v2_5",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.75,
                        "style": 0.1,
                        "use_speaker_boost": True
                    }
                }
                response = requests.post(url, json=data, headers=headers, timeout=10)
                if response.status_code == 200:
                    audio_bytes = response.content
                    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
                    engine_type = "ElevenLabs HD Voice Engine (eleven_turbo_v2_5)"
                else:
                    print(f"[ElevenLabs] HTTP {response.status_code}: {response.text}")
            except Exception as e:
                print(f"[ElevenLabs] Synthesis error: {e}")

        duration_ms = (time.perf_counter() - start_time) * 1000

        return {
            "has_audio_stream": bool(audio_base64),
            "audio_base64": audio_base64,
            "engine": engine_type,
            "character_count": character_count,
            "duration_ms": round(duration_ms, 2),
            "voice_id": self.voice_id,
            "text": text
        }

voice_engine = VoiceEngine()
