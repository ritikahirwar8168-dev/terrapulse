# 🌿 Hackathon Submission Post: TerraPulse

**Project Name:** TerraPulse — Screenless Outdoor & Trail Agent  
**Theme:** Touch Grass  
**Primary Open Source Core:** Google Gemma 2 (Open-weight model) + Prior Labs TabPFN (Tabular foundation model)  

---

### 🌟 What We Built
We built **TerraPulse**, a screenless outdoor companion engineered around a single rule: **the screen must be the shortest part of the experience (< 30 seconds).**

Hikers, trail runners, foragers, and gardeners frequently face unpredictable conditions (slippery mud, hidden black ice, wet leaf litter, or frost). Instead of scrolling endless apps, TerraPulse takes local microclimate and soil telemetry (temperature, humidity, soil moisture, elevation, canopy density, and rainfall hours), executes high-speed tabular prediction using **Prior Labs TabPFN**, reasons through the trail physics using **Google Gemma 2**, and produces an audio field briefing narrated by **ElevenLabs**.

You hit one button, listen to 15 seconds of crisp advice, **put your phone into your pocket**, and spend the next hour immersed in nature with a tangible physical micro-quest (e.g. *"Find 3 distinct wild fungi varieties on shaded oak trunks"*).

---

### 💡 Why Open Innovation Matters for What We Built
Out on mountain ridges, remote hiking loops, and forest reserves, **cellular reception drops to zero**. 

If an outdoor tool relies on closed, proprietary cloud APIs (OpenAI or Claude), **it will fail the moment you actually step into nature**. 

Open-source and open-weight AI fundamentally changes this equation:
1. **True Edge Sovereignty:** With open-weight models like **Google Gemma 2** and tabular foundation models like **Prior Labs TabPFN**, inference can run locally on an edge laptop or mobile runtime without internet connectivity.
2. **Absolute Privacy:** Environmental and precise GPS/trail coordinates stay strictly on the user's local device without being broadcast to external corporate servers.
3. **Zero Marginal Cost:** Nature should be accessible to everyone—open models eliminate per-token paywalls for trail runners and community gardeners.

---

### 🛠️ Prize Categories Addressed

- **Best Use of Gemma ($200):** Google's open-weight **Gemma 2** (`gemma-2-9b-it`) serves as the core field naturalist agent, transforming tabular predictions into mindful, screen-free missions.
- **Best Use of TabPFN ($200):** Prior Labs' **TabPFN** tabular foundation model classifies microclimate features into trail conditions and frost hazard probabilities with zero training time.
- **Best Use of Render ($200):** Configured with `render.yaml` for 1-click cloud runtime deployment.
- **Best Use of ElevenLabs ($100):** Powers natural voice narration so users explore hands-free without looking at their screens.
- **Best Use of Sentry ($100):** Fully instrumented with `sentry-sdk` custom agent tracing, profiling latency across `tabpfn.inference`, `gemma.reasoning`, and `elevenlabs.tts_stream`.

---

### 🚀 Running the Project
- **Local:** `python app.py` ➔ Open `http://localhost:8000`
- **Deploy on Render:** Push repository and connect via `render.yaml`
