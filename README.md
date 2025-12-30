# Dreamy Vision

See the hidden figures in patterns.

A web application that helps users visualize hidden figures in patterns by drawing what they see and using AI to enhance the pattern.

## Project Structure

```
dreamy-vision/
├── web-demo/          # Frontend (HTML/CSS/JS)
│   ├── index.html
│   ├── draw.html
│   ├── result.html
│   ├── css/
│   ├── js/
│   └── assets/
│
└── backend/           # FastAPI backend
    ├── app/
    │   ├── main.py
    │   ├── config.py
    │   ├── models/
    │   └── utils/
    └── requirements.txt
```

## Quick Start

### Backend (Mac Studio M2 Max)

1. Navigate to backend:
```bash
cd backend
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Web Demo

1. Navigate to web-demo:
```bash
cd web-demo
```

2. Serve with local server:
```bash
python3 -m http.server 8080
```

3. Open `http://localhost:8080` in browser

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript (Vanilla JS)
- **Backend**: FastAPI (Python)
- **AI**: Stable Diffusion 1.5 + ControlNet
- **LLM**: Ollama / OpenAI / Hugging Face (for prompt enhancement)
- **Deployment**: Local (Mac Studio M2 Max)

## Features

- Upload pattern images
- Draw what you see
- AI-enhanced pattern visualization
- LLM-powered prompt enhancement
- AI hint generation (`/hint` endpoint)
- Download results

## LLM Integration

Dreamy Vision supports multiple LLM backends for understanding user descriptions and enhancing prompts:

- **Ollama** (recommended): Local, free, private
- **OpenAI API**: Cloud-based, high quality
- **Hugging Face**: Fully customizable local models

See [backend/LLM_SETUP.md](backend/LLM_SETUP.md) for detailed setup instructions.

## Development Status

🚧 **In Development** - MVP phase

## License

Hobby project - feel free to use and modify

