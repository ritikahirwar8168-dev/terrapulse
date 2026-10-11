// TerraPulse Frontend Application Logic
let currentActivity = 'hiking';
let currentAudio = null;
let currentBriefingText = "";
let isPlaying = false;

// DOM Elements
const activityBtns = document.querySelectorAll('.activity-btn');
const presetPills = document.getElementById('presetPills');
const locNameInput = document.getElementById('locName');
const tempInput = document.getElementById('tempInput');
const moistInput = document.getElementById('moistInput');
const humInput = document.getElementById('humInput');
const elevInput = document.getElementById('elevInput');
const rainInput = document.getElementById('rainInput');
const canopyInput = document.getElementById('canopyInput');

const tempVal = document.getElementById('tempVal');
const moistVal = document.getElementById('moistVal');
const humVal = document.getElementById('humVal');
const elevVal = document.getElementById('elevVal');
const rainVal = document.getElementById('rainVal');
const canopyVal = document.getElementById('canopyVal');

const analyzeBtn = document.getElementById('analyzeBtn');
const grassScoreText = document.getElementById('grassScoreText');
const trailConditionText = document.getElementById('trailConditionText');
const trailConfText = document.getElementById('trailConfText');
const frostRiskText = document.getElementById('frostRiskText');
const frostConfText = document.getElementById('frostConfText');
const briefingQuote = document.getElementById('briefingQuote');
const microQuestText = document.getElementById('microQuestText');
const sensoryAnchorText = document.getElementById('sensoryAnchorText');
const voiceEngineBadge = document.getElementById('voiceEngineBadge');

const playAudioBtn = document.getElementById('playAudioBtn');
const playIcon = document.getElementById('playIcon');
const audioProgressBar = document.getElementById('audioProgressBar');
const audioStatusText = document.getElementById('audioStatusText');

const spansContainer = document.getElementById('spansContainer');
const traceSummaryBar = document.getElementById('traceSummaryBar');
const traceSessionId = document.getElementById('traceSessionId');
const traceLatency = document.getElementById('traceLatency');
const traceTokens = document.getElementById('traceTokens');

// Slider live updates
tempInput.addEventListener('input', (e) => tempVal.textContent = e.target.value);
moistInput.addEventListener('input', (e) => moistVal.textContent = e.target.value);
humInput.addEventListener('input', (e) => humVal.textContent = e.target.value);
elevInput.addEventListener('input', (e) => elevVal.textContent = e.target.value);
rainInput.addEventListener('input', (e) => rainVal.textContent = e.target.value);
canopyInput.addEventListener('input', (e) => canopyVal.textContent = e.target.value);

// Activity Mode toggles
activityBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    activityBtns.forEach(b => {
      b.classList.remove('active', 'border-stone-700', 'bg-stone-800/90');
      b.classList.add('border-stone-800', 'bg-stone-900/60');
    });
    btn.classList.add('active', 'border-stone-700', 'bg-stone-800/90');
    btn.classList.remove('border-stone-800', 'bg-stone-900/60');
    currentActivity = btn.dataset.mode;
  });
});

// Load Presets
async function loadPresets() {
  try {
    const res = await fetch('/api/presets');
    const data = await res.json();
    presetPills.innerHTML = '';
    data.presets.forEach(p => {
      const pill = document.createElement('button');
      pill.className = 'text-xs px-3 py-1.5 rounded-lg bg-stone-800 hover:bg-stone-700 text-stone-300 border border-stone-700/60 transition-colors flex items-center gap-1.5 cursor-pointer';
      pill.innerHTML = `<i class="fa-solid fa-map-pin text-emerald-400 text-[10px]"></i> ${p.name.split(' (')[0]}`;
      pill.addEventListener('click', () => applyPreset(p));
      presetPills.appendChild(pill);
    });
  } catch (err) {
    console.error('Failed to load presets:', err);
  }
}

function applyPreset(p) {
  locNameInput.value = p.name;
  tempInput.value = p.temperature_c; tempVal.textContent = p.temperature_c;
  moistInput.value = p.soil_moisture_pct; moistVal.textContent = p.soil_moisture_pct;
  humInput.value = p.humidity_pct; humVal.textContent = p.humidity_pct;
  elevInput.value = p.elevation_m; elevVal.textContent = p.elevation_m;
  rainInput.value = p.hours_since_rain; rainVal.textContent = p.hours_since_rain;
  canopyInput.value = p.canopy_cover_pct; canopyVal.textContent = p.canopy_cover_pct;

  // Set activity
  if (p.activity_mode) {
    activityBtns.forEach(b => {
      if (b.dataset.mode === p.activity_mode) {
        b.click();
      }
    });
  }
}

// Run Analysis
analyzeBtn.addEventListener('click', async () => {
  analyzeBtn.disabled = true;
  analyzeBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Synthesizing Field Intelligence...`;

  const payload = {
    location_name: locNameInput.value,
    temperature_c: parseFloat(tempInput.value),
    humidity_pct: parseFloat(humInput.value),
    soil_moisture_pct: parseFloat(moistInput.value),
    elevation_m: parseFloat(elevInput.value),
    hours_since_rain: parseFloat(rainInput.value),
    canopy_cover_pct: parseFloat(canopyInput.value),
    wind_speed_kmh: 12.0,
    activity_mode: currentActivity
  };

  try {
    const res = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    renderResults(data);
  } catch (err) {
    alert('Analysis failed: ' + err.message);
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = `<i class="fa-solid fa-play"></i> Synthesize Briefing & Touch Grass`;
  }
});

function renderResults(data) {
  const tabpfn = data.tabpfn_result;
  const gemma = data.gemma_briefing;
  const voice = data.voice_narration;
  const sentry = data.sentry_trace;

  // 1. Metrics & TabPFN
  grassScoreText.textContent = `${tabpfn.grass_score}%`;
  trailConditionText.textContent = tabpfn.trail_condition;
  trailConfText.textContent = `${tabpfn.trail_confidence}% Conf (${tabpfn.foundation_engine})`;
  frostRiskText.textContent = tabpfn.frost_risk;
  frostConfText.textContent = `${tabpfn.frost_confidence}% Model Conf`;

  // Color code grass score
  if (tabpfn.grass_score > 75) {
    grassScoreText.className = "text-3xl font-extrabold text-lime-400";
  } else if (tabpfn.grass_score > 50) {
    grassScoreText.className = "text-3xl font-extrabold text-amber-400";
  } else {
    grassScoreText.className = "text-3xl font-extrabold text-rose-400";
  }

  // 2. Gemma Briefing
  currentBriefingText = gemma.field_briefing;
  briefingQuote.textContent = `"${currentBriefingText}"`;
  microQuestText.textContent = gemma.micro_quest;
  sensoryAnchorText.textContent = gemma.sensory_anchor;

  // 3. Audio Voice Setup
  voiceEngineBadge.textContent = voice.engine;
  if (voice.has_audio_stream && voice.audio_base64) {
    currentAudio = new Audio("data:audio/mp3;base64," + voice.audio_base64);
  } else {
    currentAudio = null; // Will fallback to Web Speech Synthesis
  }
  stopAudio();
  audioStatusText.textContent = "Click play to listen";

  // Auto-play audio once ready
  playAudio();

  // 4. Render Sentry Waterfall Spans
  renderSentryWaterfall(sentry);
}

function renderSentryWaterfall(sentry) {
  spansContainer.innerHTML = '';
  traceSummaryBar.classList.remove('hidden');
  traceSessionId.textContent = sentry.session_id;
  traceLatency.textContent = `${sentry.total_latency_ms} ms`;
  traceTokens.textContent = `${sentry.total_tokens} est`;

  const maxDuration = Math.max(...sentry.spans.map(s => s.duration_ms), 1);

  sentry.spans.forEach(span => {
    const widthPct = Math.max(12, Math.min(100, (span.duration_ms / maxDuration) * 100));
    const spanEl = document.createElement('div');
    spanEl.className = 'bg-stone-950 p-2.5 rounded-lg border border-stone-800/80 space-y-1.5';
    
    let badgeColor = 'bg-blue-500/10 text-blue-400 border-blue-500/20';
    if (span.category.includes('tabpfn')) badgeColor = 'bg-violet-500/10 text-violet-400 border-violet-500/20';
    if (span.category.includes('elevenlabs')) badgeColor = 'bg-amber-500/10 text-amber-400 border-amber-500/20';

    spanEl.innerHTML = `
      <div class="flex justify-between items-center text-[11px]">
        <div class="flex items-center gap-2">
          <span class="px-1.5 py-0.5 rounded text-[10px] font-mono border ${badgeColor}">${span.category}</span>
          <span class="font-medium text-stone-200">${span.name}</span>
        </div>
        <span class="font-mono text-stone-400">${span.duration_ms} ms</span>
      </div>
      <div class="h-1.5 rounded-full bg-stone-900 overflow-hidden">
        <div class="h-full bg-gradient-to-r from-emerald-500 to-lime-400 rounded-full" style="width: ${widthPct}%"></div>
      </div>
    `;
    spansContainer.appendChild(spanEl);
  });
}

// Audio controls
playAudioBtn.addEventListener('click', () => {
  if (isPlaying) {
    stopAudio();
  } else {
    playAudio();
  }
});

function playAudio() {
  if (!currentBriefingText) return;

  if (currentAudio) {
    currentAudio.play();
    isPlaying = true;
    playIcon.className = "fa-solid fa-pause ml-0";
    audioStatusText.textContent = "Narrating via ElevenLabs...";
    currentAudio.ontimeupdate = () => {
      const pct = (currentAudio.currentTime / currentAudio.duration) * 100;
      audioProgressBar.style.width = `${pct}%`;
    };
    currentAudio.onended = () => stopAudio();
  } else if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(currentBriefingText);
    utter.rate = 0.95;
    utter.pitch = 1.0;
    utter.onstart = () => {
      isPlaying = true;
      playIcon.className = "fa-solid fa-pause ml-0";
      audioStatusText.textContent = "Speaking field briefing...";
      audioProgressBar.style.width = '50%';
    };
    utter.onend = () => stopAudio();
    utter.onerror = () => stopAudio();
    window.speechSynthesis.speak(utter);
  }
}

function stopAudio() {
  isPlaying = false;
  playIcon.className = "fa-solid fa-play ml-0.5";
  audioStatusText.textContent = "Paused / Done";
  audioProgressBar.style.width = '0%';
  if (currentAudio) {
    currentAudio.pause();
    currentAudio.currentTime = 0;
  }
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
}

// Initial load
loadPresets();
