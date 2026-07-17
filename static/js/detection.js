// ==========================================
// Airport Security AI
// Detection Page
// ==========================================

const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const previewPlaceholder = document.getElementById("previewPlaceholder");

const detectBtn = document.getElementById("detectBtn");
const uploadForm = document.getElementById("uploadForm");


// ==========================================
// Image Preview
// ==========================================

imageInput.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) return;

    const reader = new FileReader();

    reader.onload = function (e) {

        previewImage.src = e.target.result;

        previewImage.style.display = "block";

        previewPlaceholder.style.display = "none";

    };

    reader.readAsDataURL(file);

});


// ==========================================
// Detect Button
// ==========================================

uploadForm.addEventListener("submit", function () {

    detectBtn.disabled = true;

    detectBtn.innerHTML = `
        <i class="fa-solid fa-spinner fa-spin"></i>
        Detecting...
    `;

});


// ==========================================
// Clear Button
// ==========================================

document.querySelector(".btn-secondary").addEventListener("click", function () {

    previewImage.src = "";

    previewImage.style.display = "none";

    previewPlaceholder.style.display = "flex";

});