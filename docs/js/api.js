// Dreamy Vision - API Communication

const API_BASE_URL = 'http://localhost:8000'; // Change this when deploying

async function enhanceImage() {
    const loadingSection = document.getElementById('loadingSection');
    const resultSection = document.getElementById('resultSection');
    const errorSection = document.getElementById('errorSection');
    const resultImage = document.getElementById('resultImage');
    
    // Get data from sessionStorage
    const originalImage = sessionStorage.getItem('uploadedImage');
    const userDrawing = sessionStorage.getItem('userDrawing');
    const description = sessionStorage.getItem('description');
    
    if (!originalImage || !userDrawing || !description) {
        showError('Missing required data. Please start over.');
        return;
    }
    
    try {
        // Convert images to base64 if needed (they should already be)
        const requestData = {
            original_image: originalImage.split(',')[1], // Remove data:image/png;base64, prefix
            user_drawing: userDrawing.split(',')[1],
            description: description,
            enhancement_strength: 0.3
        };
        
        const response = await fetch(`${API_BASE_URL}/enhance`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Display result
        resultImage.src = `data:image/png;base64,${data.enhanced_image}`;
        loadingSection.classList.add('hidden');
        resultSection.classList.remove('hidden');
        
    } catch (error) {
        console.error('Enhancement error:', error);
        showError(`Failed to enhance image: ${error.message}`);
    }
}

function showError(message) {
    const loadingSection = document.getElementById('loadingSection');
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.querySelector('.error-message');
    const retryBtn = document.getElementById('retryBtn');
    const goBackBtn = document.getElementById('goBackBtn');
    
    errorMessage.textContent = message;
    loadingSection.classList.add('hidden');
    errorSection.classList.remove('hidden');
    
    retryBtn.addEventListener('click', () => {
        errorSection.classList.add('hidden');
        loadingSection.classList.remove('hidden');
        enhanceImage();
    });
    
    goBackBtn.addEventListener('click', () => {
        window.location.href = 'draw.html';
    });
}

// Auto-enhance when result page loads
if (document.getElementById('loadingSection')) {
    // Check if we have the data
    const originalImage = sessionStorage.getItem('uploadedImage');
    const userDrawing = sessionStorage.getItem('userDrawing');
    const description = sessionStorage.getItem('description');
    
    if (originalImage && userDrawing && description) {
        enhanceImage();
    } else {
        showError('Missing data. Please start over.');
    }
}

