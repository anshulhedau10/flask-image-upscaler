function checkInput() {
    var fileInput = document.getElementById('file');

    var filePath = fileInput.value;

    // Allowing file type
    var allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;

    if (!allowedExtensions.exec(filePath)) {
        alert('Invalid file type! Please choose an image.');
        fileInput.value = null;

        return false;
    } 

    document.getElementById('btnPress').innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
    document.getElementById('btnSubmit').disabled = true;
    document.getElementById('btnPressMsg').innerHTML = '<p>Take a sip of water 🥤.</p>'
}
