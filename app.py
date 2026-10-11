import os
import time
import uuid
from typing import Dict, Any, Optional
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from core.tabpfn_engine import tabpfn_engine
from core.gemma_agent import gemma_agent
from core.voice_engine import voice_engine
from core.sentry_tracer import tracer

app = FastAPI(
    title="TerraPulse: Screenless Outdoor & Trail Agent",
    description="Powered by Prior Labs TabPFN, Google Gemma, ElevenLabs, and Sentry for the Touch Grass Hackathon",
    version="1.0.0"
)

# Mount static files
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class EnvironmentRequest(BaseModel):
    location_name: str = "Whispering Ridge Trail"
    temperature_c: float = 18.5
    humidity_pct: float = 45.0
    soil_moisture_pct: float = 22.0
    elevation_m: float = 350.0
    hours_since_rain: float = 48.0
    canopy_cover_pct: float = 60.0
    wind_speed_kmh: float = 12.0
    activity_mode: str = "hiking" # hiking, gardening, running, foraging

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/api/presets")
async def get_presets():
    return {
        "presets": [
            {
                "id": "pine_ridge",
                "name": "Pine Ridge Trail (Dry Hardpack)",
                "temperature_c": 21.0,
                "humidity_pct": 38.0,
                "soil_moisture_pct": 18.0,
                "elevation_m": 520.0,
                "hours_since_rain": 72.0,
                "canopy_cover_pct": 35.0,
                "wind_speed_kmh": 15.0,
                "activity_mode": "hiking"
            },
            {
                "id": "creek_valley",
                "name": "Misty Creek Hollow (Slick Mud)",
                "temperature_c": 13.5,
                "humidity_pct": 85.0,
                "soil_moisture_pct": 72.0,
                "elevation_m": 240.0,
                "hours_since_rain": 3.0,
                "canopy_cover_pct": 80.0,
                "wind_speed_kmh": 7.0,
                "activity_mode": "foraging"
            },
            {
                "id": "frost_summit",
                "name": "Alpine Ridge (Early Morning Frost)",
                "temperature_c": 1.5,
                "humidity_pct": 70.0,
                "soil_moisture_pct": 50.0,
                "elevation_m": 950.0,
                "hours_since_rain": 24.0,
                "canopy_cover_pct": 40.0,
                "wind_speed_kmh": 26.0,
                "activity_mode": "running"
            },
            {
                "id": "permaculture_bed",
                "name": "Home Garden & Orchard Plot",
                "temperature_c": 19.5,
                "humidity_pct": 52.0,
                "soil_moisture_pct": 32.0,
                "elevation_m": 120.0,
                "hours_since_rain": 36.0,
                "canopy_cover_pct": 20.0,
                "wind_speed_kmh": 9.0,
                "activity_mode": "gardening"
            }
        ]
    }

@app.post("/api/analyze")
async def analyze_environment(req: EnvironmentRequest):
    session_id = str(uuid.uuid4())[:8]
    trace = tracer.start_trace(session_id=session_id, location_name=req.location_name)

    features = {
        "temperature_c": req.temperature_c,
        "humidity_pct": req.humidity_pct,
        "soil_moisture_pct": req.soil_moisture_pct,
        "elevation_m": req.elevation_m,
        "hours_since_rain": req.hours_since_rain,
        "canopy_cover_pct": req.canopy_cover_pct,
        "wind_speed_kmh": req.wind_speed_kmh
    }

    # Span 1: Prior Labs TabPFN tabular prediction
    tabpfn_res = tabpfn_engine.predict_microclimate(features)
    trace.record_span(
        name="TabPFN Tabular In-Context Inference",
        category="ai.tabpfn.tabular",
        duration_ms=tabpfn_res["inference_duration_ms"],
        metadata={
            "predicted_condition": tabpfn_res["trail_condition"],
            "trail_confidence": f"{tabpfn_res['trail_confidence']}%",
            "frost_risk": tabpfn_res["frost_risk"],
            "model": tabpfn_res["foundation_engine"]
        }
    )

    # Span 2: Google Gemma Open-Weight Reasoning
    gemma_res = gemma_agent.generate_briefing(tabpfn_res, activity_mode=req.activity_mode)
    trace.total_tokens += gemma_res["estimated_tokens"]
    trace.record_span(
        name="Gemma 2 Open-Weight Nature Reasoning",
        category="ai.gemma.llm",
        duration_ms=gemma_res["inference_duration_ms"],
        metadata={
            "model": gemma_res["model_used"],
            "estimated_tokens": gemma_res["estimated_tokens"],
            "runtime": gemma_res["open_weight_source"]
        }
    )

    # Span 3: ElevenLabs Audio Synthesis
    field_text = gemma_res["gemma_output"].get("field_briefing", "")
    voice_res = voice_engine.synthesize_briefing(field_text)
    trace.record_span(
        name="ElevenLabs Outdoor Voice Stream",
        category="ai.elevenlabs.tts",
        duration_ms=voice_res["duration_ms"],
        metadata={
            "engine": voice_res["engine"],
            "voice_id": voice_res["voice_id"],
            "character_count": voice_res["character_count"],
            "has_stream": voice_res["has_audio_stream"]
        }
    )

    completed_trace = trace.complete()

    return {
        "status": "success",
        "session_id": session_id,
        "location_name": req.location_name,
        "activity_mode": req.activity_mode,
        "tabpfn_result": tabpfn_res,
        "gemma_briefing": gemma_res["gemma_output"],
        "voice_narration": voice_res,
        "sentry_trace": completed_trace,
        "sponsor_badges": {
            "gemma": "Google Gemma Open-Weight Model",
            "tabpfn": "Prior Labs TabPFN Foundation Model",
            "elevenlabs": "ElevenLabs Natural Voice Generation",
            "sentry": "Sentry Agent Tracing & Performance Metrics",
            "render": "Render-Ready Cloud Runtime"
        }
    }

@app.get("/api/traces")
async def get_traces():
    return {"traces": tracer.recent_traces}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
