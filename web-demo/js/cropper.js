// Image Cropper - Crop to 512x512 for processing

class ImageCropper {
    constructor(imageSrc, targetSize = 512) {
        this.targetSize = targetSize;
        this.image = new Image();
        this.image.src = imageSrc;
        this.cropper = null;
        return this.init();
    }
    
    async init() {
        return new Promise((resolve) => {
            this.image.onload = () => {
                resolve(this);
            };
        });
    }
    
    createCropper(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        // Create cropper UI
        container.innerHTML = `
            <div class="cropper-container">
                <div class="cropper-info">
                    <p>Crop your image to ${this.targetSize}x${this.targetSize} pixels</p>
                    <p class="cropper-hint">Drag to select the area you want to enhance</p>
                </div>
                <div class="cropper-wrapper">
                    <canvas id="cropperCanvas"></canvas>
                    <div id="cropOverlay" class="crop-overlay"></div>
                </div>
                <div class="cropper-controls">
                    <button id="cropBtn" class="dreamy-button">Crop & Continue</button>
                    <button id="skipCropBtn" class="dreamy-button-secondary">Skip (Auto-crop center)</button>
                </div>
            </div>
        `;
        
        const canvas = document.getElementById('cropperCanvas');
        const ctx = canvas.getContext('2d');
        const overlay = document.getElementById('cropOverlay');
        
        // Set canvas size
        const maxDisplaySize = 600;
        const scale = Math.min(maxDisplaySize / this.image.width, maxDisplaySize / this.image.height);
        canvas.width = this.image.width * scale;
        canvas.height = this.image.height * scale;
        canvas.style.width = canvas.width + 'px';
        canvas.style.height = canvas.height + 'px';
        
        // Draw image
        ctx.drawImage(this.image, 0, 0, canvas.width, canvas.height);
        
        // Calculate crop area (square, centered)
        const cropSize = Math.min(canvas.width, canvas.height);
        const cropX = (canvas.width - cropSize) / 2;
        const cropY = (canvas.height - cropSize) / 2;
        
        // Draw crop overlay
        this.drawCropOverlay(ctx, cropX, cropY, cropSize);
        
        // Make draggable
        let isDragging = false;
        let startX, startY;
        let currentX = cropX;
        let currentY = cropY;
        
        canvas.addEventListener('mousedown', (e) => {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            if (x >= currentX && x <= currentX + cropSize &&
                y >= currentY && y <= currentY + cropSize) {
                isDragging = true;
                startX = x - currentX;
                startY = y - currentY;
            }
        });
        
        canvas.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left - startX;
            const y = e.clientY - rect.top - startY;
            
            // Constrain to canvas bounds
            currentX = Math.max(0, Math.min(x, canvas.width - cropSize));
            currentY = Math.max(0, Math.min(y, canvas.height - cropSize));
            
            // Redraw
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(this.image, 0, 0, canvas.width, canvas.height);
            this.drawCropOverlay(ctx, currentX, currentY, cropSize);
        });
        
        canvas.addEventListener('mouseup', () => {
            isDragging = false;
        });
        
        // Crop button
        document.getElementById('cropBtn').addEventListener('click', () => {
            this.crop(currentX, currentY, cropSize, scale);
        });
        
        // Skip button (auto-crop center)
        document.getElementById('skipCropBtn').addEventListener('click', () => {
            this.crop(cropX, cropY, cropSize, scale);
        });
    }
    
    drawCropOverlay(ctx, x, y, size) {
        // Darken outside crop area
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        
        // Clear crop area
        ctx.clearRect(x, y, size, size);
        ctx.drawImage(this.image, x / (ctx.canvas.width / this.image.width), 
                     y / (ctx.canvas.height / this.image.height), 
                     size / (ctx.canvas.width / this.image.width),
                     size / (ctx.canvas.height / this.image.height),
                     x, y, size, size);
        
        // Draw border
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 2;
        ctx.strokeRect(x, y, size, size);
        
        // Draw corner handles
        const handleSize = 10;
        ctx.fillStyle = '#fff';
        // Top-left
        ctx.fillRect(x - handleSize/2, y - handleSize/2, handleSize, handleSize);
        // Top-right
        ctx.fillRect(x + size - handleSize/2, y - handleSize/2, handleSize, handleSize);
        // Bottom-left
        ctx.fillRect(x - handleSize/2, y + size - handleSize/2, handleSize, handleSize);
        // Bottom-right
        ctx.fillRect(x + size - handleSize/2, y + size - handleSize/2, handleSize, handleSize);
    }
    
    crop(x, y, size, scale) {
        // Calculate actual crop coordinates on original image
        const canvas = document.getElementById('cropperCanvas');
        const scaleX = this.image.width / canvas.width;
        const scaleY = this.image.height / canvas.height;
        const cropX = x * scaleX;
        const cropY = y * scaleY;
        const cropSize = size * Math.min(scaleX, scaleY);
        
        // Create new canvas for cropped image
        const croppedCanvas = document.createElement('canvas');
        croppedCanvas.width = this.targetSize;
        croppedCanvas.height = this.targetSize;
        const croppedCtx = croppedCanvas.getContext('2d');
        
        // Draw cropped and resized image
        croppedCtx.drawImage(this.image, cropX, cropY, cropSize, cropSize, 0, 0, this.targetSize, this.targetSize);
        
        // Convert to data URL and store
        const croppedDataUrl = croppedCanvas.toDataURL('image/png');
        sessionStorage.setItem('uploadedImage', croppedDataUrl);
        
        // Navigate to next page
        window.location.href = 'draw.html';
    }
}

