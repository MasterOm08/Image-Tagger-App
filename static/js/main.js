document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("imageInput");
    const previewImage = document.getElementById("imagePreview");
    const uploadText = document.getElementById("uploadText");
    const uploadForm = document.getElementById("uploadForm");
    const spinner = document.getElementById("loadingSpinner");
    const submitBtn = document.getElementById("submitBtn");

    if (fileInput) {
        fileInput.addEventListener("change", (e) => {
            const file = e.target.files[0];
            if (file) {
                // Update UI text to show chosen file name
                if (uploadText) {
                    uploadText.innerHTML = `Selected: <strong>${file.name}</strong>`;
                }
                // Show preview
                if (previewImage) {
                    previewImage.src = URL.createObjectURL(file);
                    previewImage.style.display = "block";
                }
            }
        });
    }

    if (uploadForm) {
        uploadForm.addEventListener("submit", (e) => {
            // Ensure a file is actually attached before submitting
            if (!fileInput.files || fileInput.files.length === 0) {
                e.preventDefault();
                alert("Please select an image file first.");
                return;
            }

            if (spinner && submitBtn) {
                spinner.style.display = "block";
                submitBtn.disabled = true;
                submitBtn.innerText = "Analyzing with Vision API...";
            }
        });
    }
});