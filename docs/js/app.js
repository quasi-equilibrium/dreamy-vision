// Dreamy Vision - Main App Logic

// Landing/Upload Page
if (document.getElementById('startBtn')) {
    const startBtn = document.getElementById('startBtn');
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const uploadBox = document.querySelector('.upload-box');
    const previewArea = document.getElementById('previewArea');
    const previewImage = document.getElementById('previewImage');
    const continueBtn = document.getElementById('continueBtn');
    
    startBtn.addEventListener('click', () => {
        startBtn.classList.add('hidden');
        uploadArea.classList.remove('hidden');
    });
    
    // File input click
    uploadBox.addEventListener('click', () => {
        fileInput.click();
    });
    
    // Drag and drop
    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.style.borderColor = 'rgba(255, 255, 255, 0.8)';
    });
    
    uploadBox.addEventListener('dragleave', () => {
        uploadBox.style.borderColor = 'rgba(255, 255, 255, 0.4)';
    });
    
    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.style.borderColor = 'rgba(255, 255, 255, 0.4)';
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
    
    function handleFileSelect(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please select an image file');
            return;
        }
        
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImage.src = e.target.result;
            previewArea.classList.remove('hidden');
            uploadBox.classList.add('hidden');
            
            // Store image in sessionStorage for next page
            sessionStorage.setItem('uploadedImage', e.target.result);
        };
        reader.readAsDataURL(file);
    }
    
    continueBtn.addEventListener('click', () => {
        window.location.href = 'draw.html';
    });
}

// Drawing Page
if (document.getElementById('descriptionInput')) {
    const descriptionInput = document.getElementById('descriptionInput');
    const submitDescription = document.getElementById('submitDescription');
    const drawingSection = document.getElementById('drawingSection');
    
    // Load image from sessionStorage
    const patternImage = document.getElementById('patternImage');
    const uploadedImage = sessionStorage.getItem('uploadedImage');
    
    if (uploadedImage) {
        patternImage.src = uploadedImage;
    } else {
        // No image found, redirect to start
        window.location.href = 'index.html';
    }
    
    submitDescription.addEventListener('click', () => {
        const description = descriptionInput.value.trim();
        if (description) {
            sessionStorage.setItem('description', description);
            descriptionInput.disabled = true;
            submitDescription.disabled = true;
            drawingSection.classList.remove('hidden');
            
            // Initialize canvas after image loads
            patternImage.onload = () => {
                initCanvas();
            };
        }
    });
    
    descriptionInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            submitDescription.click();
        }
    });
}

// Result Page
if (document.getElementById('resultSection')) {
    // This will be handled by api.js when enhancement is complete
    const tryAgainBtn = document.getElementById('tryAgainBtn');
    const startOverBtn = document.getElementById('startOverBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    
    tryAgainBtn.addEventListener('click', () => {
        // Regenerate with same inputs
        window.location.reload();
    });
    
    startOverBtn.addEventListener('click', () => {
        sessionStorage.clear();
        window.location.href = 'index.html';
    });
    
    downloadBtn.addEventListener('click', () => {
        const resultImage = document.getElementById('resultImage');
        const link = document.createElement('a');
        link.download = 'dreamy-vision-result.png';
        link.href = resultImage.src;
        link.click();
    });
}

