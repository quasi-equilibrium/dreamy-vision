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

### Time Series Foundation Models (for stocks, crypto, etc.)

| Model | Params | Best For |
|-------|--------|----------|
| **Chronos-2** | 120M | Multivariate, covariates, SOTA |
| **Chronos-Bolt** | 9M–205M | Fast, zero-shot, single series |
| **Google TimesFM** | 200M–500M | Univariate, long context |
| Chronos T5 | 46M–710M | Legacy option |

### Chronos-2 (multivariate + covariates)

```python
pip install "chronos-forecasting>=2.0"
from chronos import Chronos2Pipeline
pipeline = Chronos2Pipeline.from_pretrained("amazon/chronos-2", device_map="cuda")
```

### Chronos-Bolt (fast, simple)

```python
pip install autogluon
from autogluon.timeseries import TimeSeriesPredictor, TimeSeriesDataFrame
# df: item_id, timestamp, target
predictor = TimeSeriesPredictor(prediction_length=24).fit(df, hyperparameters={"Chronos": {"model_path": "autogluon/chronos-bolt-small"}})
predictions = predictor.predict(df)
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
| Trade/crypto forecast | Chronos-2, Chronos-Bolt |
| Polymarket 5-min BTC | LightGBM classifier + Polymarket odds |
