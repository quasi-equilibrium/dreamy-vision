# Dreamy Vision - Web Demo

Web frontend for Dreamy Vision pattern enhancement app.

## Setup

1. Open `index.html` in a web browser, or

2. Serve with a local server (recommended):
```bash
# Python 3
python3 -m http.server 8080

# Node.js (if you have it)
npx http-server -p 8080
```

3. Open `http://localhost:8080` in your browser

## Configuration

Update the API URL in `js/api.js`:
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

Change this to your backend server URL when deploying.

## Pages

- `index.html` - Landing/upload page
- `draw.html` - Drawing canvas
- `result.html` - Result display

## Features

- Image upload (drag & drop or click)
- Drawing canvas with pen tool
- Undo/Reset functionality
- Real-time drawing on pattern
- API integration for enhancement

## Browser Compatibility

Works in modern browsers (Chrome, Firefox, Safari, Edge)

