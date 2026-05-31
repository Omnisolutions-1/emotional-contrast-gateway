# Emotional Contrast Gateway

A lightweight, pre-AI micro-agent pipeline and tone routing engine designed for enterprise LLM deployments. This framework normalizes human emotional indicators and parses literal intents to protect AI models from "Model Collapse" and conversational warping caused by chaotic, unstructured input data.

## 🏗️ Core Architecture

The gateway processes incoming human communication across a multi-layer segregation pipeline before it ever reaches a primary Large Language Model:

### 1. Pipeline Layer (`src/pipeline/`)
* **Tone Matrix Sensor:** Tracks human emotional indicators (joy, grief, sarcasm) on a relative coordinate grid, normalizing emotional weights to prevent code scaling errors.
* **Literal Intent Parser:** Cleanses text data by scrubbing out conversational noise phrases, unneeded emotional punctuation, and irregular spacing to expose raw requests.
* **Paradox Guard:** Maps the variance between emotional intensity and sentence complexity, triggering alert states when a structural cognitive paradox is detected.

### 2. Routing Layer (`src/routing/`)
* **Dynamic Context Router:** Automatically maps the normalized tone and paradox metrics against an enterprise parameter registry. It dynamically shifts LLM parameters (temperature, top_p) and appends specialized behavioral instructions based on real-time human cognitive states.

---

## 🛠️ Repository Layout

```text
emotional-contrast-gateway/
│
├── config.json                 # Mode profiles and parameter registries
├── telemetry_runner.py          # Execution and integration test suite
│
└── src/
    ├── __init__.py
    ├── pipeline/
    │   ├── __init__.py
    │   ├── tone_sensor.py      # Layer 1A: ToneMatrixSensor
    │   ├── intent_parser.py    # Layer 1B: LiteralIntentParser
    │   └── paradox_guard.py    # Layer 1C: ParadoxGuard
    │
    └── routing/
        ├── __init__.py
        └── context_router.py   # Layer 2: DynamicContextRouter
```

---

## 🚀 Quick Start & Testing

Execute the test suite locally to verify the normalized mode-flipping bounds and polite command-routing regex windows:

```bash
python telemetry_runner.py
```
