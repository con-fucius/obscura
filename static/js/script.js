// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');
    const dropArea = document.getElementById('drop-area');
    const filePreviewContainer = document.getElementById('file-preview-container');
    const filePreview = document.getElementById('file-preview');
    const removeFileButton = document.getElementById('remove-file');
    const processButton = document.getElementById('process-button');
    const loader = document.querySelector('.loader');
    const results = document.getElementById('results');
    const tryAnotherButton = document.getElementById('try-another');
    const errorMessage = document.getElementById('error-message');

    // Handle drag and drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropArea.style.backgroundColor = 'rgba(0, 168, 232, 0.1)';
        dropArea.style.borderColor = 'var(--primary-color)';
    }

    function unhighlight() {
        dropArea.style.backgroundColor = '';
        dropArea.style.borderColor = '';
    }

    dropArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length) {
            fileInput.files = files;
            updateFilePreview();
        }
    }

    // Handle file selection
    fileInput.addEventListener('change', updateFilePreview);

    function updateFilePreview() {
        if (fileInput.files && fileInput.files.length > 0) {
            // For multiple files, we'll just show the first one as a preview
            const file = fileInput.files[0];
            
            if (!file.type.match('image.*')) {
                showError('Please select image files (JPEG, PNG, GIF).');
                resetForm();
                return;
            }

            const reader = new FileReader();
            reader.onload = function(e) {
                filePreview.src = e.target.result;
                dropArea.classList.add('hidden');
                filePreviewContainer.classList.remove('hidden');
                processButton.disabled = false;
                hideError();
            };
            reader.readAsDataURL(file);
        }
    }

    // Remove selected file
    removeFileButton.addEventListener('click', resetForm);

    function resetForm() {
        fileInput.value = '';
        filePreview.src = '';
        dropArea.classList.remove('hidden');
        filePreviewContainer.classList.add('hidden');
        processButton.disabled = true;
    }

    // Handle form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (!fileInput.files || fileInput.files.length === 0) {
            showError('Please select one or more images to process.');
            return;
        }

        form.classList.add('hidden');
        loader.classList.remove('hidden');
        results.innerHTML = ''; // Clear previous results
        results.classList.add('hidden');
        hideError();

        const formData = new FormData();
        for (const file of fileInput.files) {
            formData.append('file', file);
        }

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loader.classList.add('hidden');
            
            if (data.error) {
                showError(data.error);
                form.classList.remove('hidden');
                return;
            }

            displayResults(data);
        })
        .catch(error => {
            loader.classList.add('hidden');
            form.classList.remove('hidden');
            showError('An error occurred during processing. Please try again.');
            console.error('Error:', error);
        });
    });

    function displayResults(data) {
        results.innerHTML = ''; // Clear previous results
        data.forEach(result => {
            const resultDiv = document.createElement('div');
            resultDiv.classList.add('result-item');

            if (result.success) {
                resultDiv.innerHTML = `
                    <div class="result-message">${result.message}</div>
                    <div class="image-comparison">
                        <div class="image-container">
                            <h3>Original Image</h3>
                            <img src="/static${result.original_image}">
                        </div>
                        <div class="image-container">
                            <h3>Processed Image</h3>
                            <img src="/static${result.processed_image}">
                            <a href="/static${result.processed_image}" class="download-button" download>
                                <i class="fas fa-download"></i> Download
                            </a>
                        </div>
                    </div>
                `;
            } else {
                resultDiv.innerHTML = `<div class="error-message">${result.filename}: ${result.error}</div>`;
            }
            results.appendChild(resultDiv);
        });
        results.classList.remove('hidden');
        results.appendChild(tryAnotherButton);
    }

    // Try another image
    tryAnotherButton.addEventListener('click', function() {
        results.classList.add('hidden');
        resetForm();
        form.classList.remove('hidden');
    });

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('hidden');
    }

    function hideError() {
        errorMessage.textContent = '';
        errorMessage.classList.add('hidden');
    }
});