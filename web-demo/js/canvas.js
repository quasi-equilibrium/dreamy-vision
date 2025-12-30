// Dreamy Vision - Canvas Drawing Functionality

let canvas, ctx;
let isDrawing = false;
let strokeHistory = [];
let currentStroke = [];

function initCanvas() {
    canvas = document.getElementById('drawingCanvas');
    if (!canvas) return;
    
    ctx = canvas.getContext('2d');
    const patternImage = document.getElementById('patternImage');
    
    // Set canvas size to match image
    canvas.width = patternImage.offsetWidth;
    canvas.height = patternImage.offsetHeight;
    
    // Set drawing style
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 3;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    
    setupEventListeners();
    updateButtonStates();
}

function setupEventListeners() {
    const undoBtn = document.getElementById('undoBtn');
    const resetBtn = document.getElementById('resetBtn');
    const okBtn = document.getElementById('okBtn');
    
    // Mouse events
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);
    
    // Touch events
    canvas.addEventListener('touchstart', handleTouch);
    canvas.addEventListener('touchmove', handleTouch);
    canvas.addEventListener('touchend', stopDrawing);
    
    undoBtn.addEventListener('click', undo);
    resetBtn.addEventListener('click', reset);
    okBtn.addEventListener('click', proceedToEnhancement);
}

function handleTouch(e) {
    e.preventDefault();
    const touch = e.touches[0];
    const mouseEvent = new MouseEvent(e.type === 'touchstart' ? 'mousedown' : 
                                      e.type === 'touchmove' ? 'mousemove' : 'mouseup', {
        clientX: touch.clientX,
        clientY: touch.clientY
    });
    canvas.dispatchEvent(mouseEvent);
}

function getMousePos(e) {
    const rect = canvas.getBoundingClientRect();
    return {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
    };
}

function startDrawing(e) {
    isDrawing = true;
    const pos = getMousePos(e);
    currentStroke = [pos];
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
}

function draw(e) {
    if (!isDrawing) return;
    
    const pos = getMousePos(e);
    currentStroke.push(pos);
    
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
}

function stopDrawing() {
    if (!isDrawing) return;
    
    isDrawing = false;
    if (currentStroke.length > 0) {
        strokeHistory.push(currentStroke);
        currentStroke = [];
        updateButtonStates();
    }
}

function undo() {
    if (strokeHistory.length === 0) return;
    
    // Redraw all strokes except the last one
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    strokeHistory.pop();
    
    strokeHistory.forEach(stroke => {
        if (stroke.length > 0) {
            ctx.beginPath();
            ctx.moveTo(stroke[0].x, stroke[0].y);
            for (let i = 1; i < stroke.length; i++) {
                ctx.lineTo(stroke[i].x, stroke[i].y);
            }
            ctx.stroke();
        }
    });
    
    updateButtonStates();
}

function reset() {
    if (confirm('Clear all drawing?')) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        strokeHistory = [];
        currentStroke = [];
        updateButtonStates();
    }
}

function updateButtonStates() {
    const undoBtn = document.getElementById('undoBtn');
    const okBtn = document.getElementById('okBtn');
    
    undoBtn.disabled = strokeHistory.length === 0;
    okBtn.disabled = strokeHistory.length === 0;
}

function proceedToEnhancement() {
    // Get drawing as image data
    const drawingData = canvas.toDataURL('image/png');
    
    // Store in sessionStorage
    sessionStorage.setItem('userDrawing', drawingData);
    
    // Navigate to result page (which will trigger enhancement)
    window.location.href = 'result.html';
}

// Export for use in other scripts
window.getDrawingData = function() {
    return canvas ? canvas.toDataURL('image/png') : null;
};

