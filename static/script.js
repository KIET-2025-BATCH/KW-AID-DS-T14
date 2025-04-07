document.getElementById('upload-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData();
    const fileInput = document.getElementById('image-input');
    const submitButton = document.querySelector('button[type="submit"]');

    if (!fileInput.files[0]) {
        alert('Please select an image file.');
        return;
    }

    submitButton.textContent = 'Processing...';
    submitButton.disabled = true;

    formData.append('image', fileInput.files[0]);

    fetch('/dehaze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('original-image').src = data.original_image;
        document.getElementById('dehazed-image').src = data.dehazed_image;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing the image. Please try again.');
    })
    .finally(() => {
        submitButton.textContent = 'Dehaze Image';
        submitButton.disabled = false;
    });
});