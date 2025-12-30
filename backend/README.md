# Dreamy Vision - Backend

FastAPI backend for Dreamy Vision pattern enhancement.

## Setup

1. Install Python 3.9+ (recommended: 3.10 or 3.11)

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
# or
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET `/`
Health check - returns API status

### GET `/health`
Health check endpoint

### POST `/enhance`
Enhance pattern image using user's drawing

**Request Body:**
```json
{
  "original_image": "base64_encoded_image",
  "user_drawing": "base64_encoded_drawing",
  "description": "what user sees",
  "enhancement_strength": 0.3
}
```

**Response:**
```json
{
  "enhanced_image": "base64_encoded_result",
  "processing_time": 12.5
}
```

## Notes

- First run will download AI models (several GB)
- Models are cached after first download
- Processing happens on local Mac Studio M2 Max
- Images are processed and deleted immediately (no storage)

## Troubleshooting

- If MPS (Metal) doesn't work, models will fall back to CPU (slower)
- Ensure you have enough disk space for model downloads (~10GB)
- For M2 Max, MPS should work automatically

