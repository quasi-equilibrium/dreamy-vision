# Models & Markets Notes

Consolidated notes from model research and Polymarket BTC 5-min market exploration.

---

## 1. Dreamy Vision Backend – Model Upgrades

### Current (Outdated)
- **Image:** SD 1.5 (`runwayml/stable-diffusion-v1-5`), ControlNet Canny
- **LLM:** mistral / llama2 (docs)
- **Packages:** diffusers 0.21.4, torch 2.1.0

### Recommended Upgrades

| Component | Quick Fix | Full Upgrade |
|-----------|-----------|--------------|
| ControlNet | Canny → Lineart | Test HED for softer edges |
| SD Base | Keep 1.5 | SDXL or SD 2.1 |
| Ollama LLM | Docs: llama3.1 / qwen2.5 | Add model selection in config |
| Packages | Relax versions | Upgrade to latest stable |

See `backend/MODEL_UPGRADE_RECOMMENDATIONS.md` for details.

---

## 2. M2 Max Mac Studio (32GB) – Highest Models

### Image Generation

| Model | Size | Fits 32GB? |
|-------|------|------------|
| **FLUX.2-klein-4B** | ~7GB | ✅ Best – newest (Jan 2026), Apache 2.0 |
| **FLUX.2-klein-9B** | ~17GB | ✅ Better quality, gated access |
| FLUX.2-dev | 60GB | ❌ Too large |
| SDXL | ~7GB | ✅ Safe alternative |

**Recommended:** `black-forest-labs/FLUX.2-klein-4B` or `FLUX.2-klein-9B`  
Requires `diffusers` 0.32+ and `Flux2KleinPipeline`.

### LLM (Ollama)

| Model | Size | Use |
|-------|------|-----|
| **Qwen 2.5 32B** | ~18–20GB | Best balance – safe |
| Llama 3.1 70B (Q2) | ~28–30GB | Pushing limit – risky |
| Llama 3.1 8B | ~4.5GB | Fast, safe |

**Suggested:** `ollama pull qwen2.5:32b`

---

## 3. GLONET – Ocean Forecasting

**Model:** `mercator-ocean/GLONET`  
**Purpose:** 10-day global ocean forecasts (temperature, salinity, currents, sea surface height).

### Usage

```bash
pip install torch torchvision xarray netCDF4 h5netcdf matplotlib huggingface_hub numpy
```

```python
from huggingface_hub import hf_hub_download
import torch

REPO_ID = "mercator-ocean/GLONET"

# Download model + normalization stats
paths = {k: hf_hub_download(repo_id=REPO_ID, filename=v, repo_type="model")
         for k, v in {"model": "weights/glonet_p1.pt", "reference": "weights/reference/ref1.nc", ...}.items()}

model = torch.jit.load(paths["model"], map_location="cuda" if torch.cuda.is_available() else "cpu")
# Input: (time=2, channels=5, lat, lon) – zos, thetao, so, uo, vo
```

See `run_GLONET.ipynb` in the repo for full workflow.

---

## 4. Trade / Market Forecasting Models

### Google TimesFM (Simple Overview)

**What it is:** A time series model from Google Research. You give it past values, it predicts future values. No training needed.

**Repo:** https://github.com/google-research/timesfm

| Version | Params | Context | Horizon |
|---------|--------|---------|---------|
| **2.5** (latest) | 200M | 16k steps | Up to 1k |
| 2.0 | 500M | 2k | Any |

**Main features:**
- Zero-shot (use as-is)
- Point forecasts + quantile forecasts (uncertainty)
- Optional covariates (extra variables)
- PyTorch or Flax

**Install:**
```bash
git clone https://github.com/google-research/timesfm.git && cd timesfm
uv venv && source .venv/bin/activate
uv pip install -e .[torch]
```

**Minimal example:**
```python
import timesfm
import numpy as np

model = timesfm.TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")
model.compile(timesfm.ForecastConfig(max_context=1024, max_horizon=256))

# Input: list of 1D arrays (your time series)
point, quantiles = model.forecast(horizon=12, inputs=[np.array([1,2,3,...])])
# point = predicted values, quantiles = percentiles
```

**Hugging Face:** https://huggingface.co/collections/google/timesfm-release-66e4be5fdb56e960c1e482a6

---

### Other Options (Quick Compare)

| Model | Params | Best For |
|-------|--------|----------|
| **Chronos-2** | 120M | Multiple variables, covariates |
| **Chronos-Bolt** | 9M–205M | Fast, single series |
| **TimesFM** | 200M | Long context, quantiles |

**Chronos-Bolt (simplest):**
```python
pip install autogluon
from autogluon.timeseries import TimeSeriesPredictor, TimeSeriesDataFrame
predictor = TimeSeriesPredictor(prediction_length=24).fit(df, hyperparameters={"Chronos": {"model_path": "autogluon/chronos-bolt-small"}})
predictions = predictor.predict(df)
```

**Chronos-2 (multivariate):**
```python
pip install "chronos-forecasting>=2.0"
from chronos import Chronos2Pipeline
pipeline = Chronos2Pipeline.from_pretrained("amazon/chronos-2", device_map="cuda")
```

---

## 5. Polymarket BTC 5-Min Up/Down Markets

### Market Structure
- **Question:** Will BTC go Up or Down in a 5-minute window?
- **Resolution:** Up if end price ≥ start price (Chainlink BTC/USD)
- **Data source:** https://data.chain.link/streams/btc-usd

### Approach

1. **Classifier (recommended):** XGBoost/LightGBM on features (returns, volatility, momentum, time)
2. **Time series models:** Chronos-Bolt for price forecast → derive Up/Down
3. **Mispricing:** Compare model P(Up) vs Polymarket odds → trade when edge > fee

### With 1 Year of Data (~105k markets)

| Use Case | Feasible |
|----------|----------|
| Train classifier (LightGBM/XGBoost) | ✅ |
| Sequence model (LSTM/Transformer) | ✅ |
| Fine-tune Chronos on price series | ✅ |
| Include Polymarket odds as feature | ✅ |
| Time-split backtest | ✅ |

### Data Format

| Column | Example |
|--------|---------|
| window_start | 2025-01-15 14:55:00 |
| window_end | 2025-01-15 15:00:00 |
| price_start | 43250.50 |
| price_end | 43280.20 |
| outcome | Up |
| return_1m, return_5m, volatility_15m | ... |
| poly_odds_up (if available) | 0.52 |

### APIs
- **Gamma API:** `https://gamma-api.polymarket.com/events?slug=btc-updown-5m-{timestamp}`
- **Chainlink:** https://data.chain.link/feeds/btc-usd

---

## Quick Reference

| Task | Model / Tool |
|------|---------------|
| Image gen (M2 Max 32GB) | FLUX.2-klein-4B or 9B |
| LLM (Ollama) | qwen2.5:32b |
| Ocean forecast | mercator-ocean/GLONET |
| Time series (zero-shot) | TimesFM, Chronos-Bolt |
| Time series (multivariate) | Chronos-2 |
| Polymarket 5-min BTC | LightGBM + Polymarket odds |
