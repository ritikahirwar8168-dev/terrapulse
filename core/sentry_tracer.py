import time
import os
import sentry_sdk
from typing import Dict, Any, List

# Initialize real Sentry SDK if DSN provided
SENTRY_DSN = os.getenv("SENTRY_DSN", "")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        environment=os.getenv("ENVIRONMENT", "development"),
        release="terrapulse@1.0.0"
    )

class AgentTracer:
    """
    Manages end-to-end tracing for TerraPulse Agent pipeline.
    Captures:
      - TabPFN tabular prediction latency & confidence
      - Google Gemma reasoning latency & token estimation
      - ElevenLabs audio synthesis latency & audio duration
      - Sentry Agent Trace spans
    """
    def __init__(self):
        self.recent_traces: List[Dict[str, Any]] = []

    def start_trace(self, session_id: str, location_name: str) -> "TraceSession":
        return TraceSession(session_id=session_id, location_name=location_name, parent=self)

    def record_completed_trace(self, trace_data: Dict[str, Any]):
        self.recent_traces.insert(0, trace_data)
        if len(self.recent_traces) > 20:
            self.recent_traces.pop()


class TraceSession:
    def __init__(self, session_id: str, location_name: str, parent: AgentTracer):
        self.session_id = session_id
        self.location_name = location_name
        self.parent = parent
        self.start_time = time.perf_counter()
        self.spans: List[Dict[str, Any]] = []
        self.total_tokens = 0
        self.status = "SUCCESS"

    def record_span(self, name: str, category: str, duration_ms: float, metadata: Dict[str, Any] = None):
        span_entry = {
            "name": name,
            "category": category,
            "duration_ms": round(duration_ms, 2),
            "metadata": metadata or {},
            "timestamp": time.time()
        }
        self.spans.append(span_entry)

        # Also push to Sentry transaction if available
        if SENTRY_DSN:
            with sentry_sdk.start_span(op=category, description=name) as s_span:
                for k, v in (metadata or {}).items():
                    s_span.set_data(k, str(v))

    def complete(self) -> Dict[str, Any]:
        total_duration_ms = round((time.perf_counter() - self.start_time) * 1000, 2)
        trace_summary = {
            "session_id": self.session_id,
            "location_name": self.location_name,
            "total_latency_ms": total_duration_ms,
            "total_tokens": self.total_tokens,
            "status": self.status,
            "spans": self.spans,
            "sentry_tracked": bool(SENTRY_DSN),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.parent.record_completed_trace(trace_summary)
        return trace_summary

tracer = AgentTracer()
