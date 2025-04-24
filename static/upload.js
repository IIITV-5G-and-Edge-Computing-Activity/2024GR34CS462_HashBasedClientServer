document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('uploadForm');
  const fileInput = document.getElementById('fileInput');
  const hashOutput = document.getElementById('hashOutput');
  const responseMessage = document.getElementById('responseMessage');
  const copyBtn = document.getElementById('copyHashBtn');

  async function computeSHA256(file) {
    const buffer = await file.arrayBuffer();
    const hashBuffer = await crypto.subtle.digest('SHA-256', buffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashBase64 = btoa(String.fromCharCode(...hashArray));
    return hashBase64;
  }

  copyBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(hashOutput.value).then(() => {
      copyBtn.textContent = 'Copied!';
      setTimeout(() => (copyBtn.textContent = 'Copy'), 1500);
    });
  });

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    const file = fileInput.files[0];
    if (!file) return;

    const hash = await computeSHA256(file);
    hashOutput.value = hash;
    copyBtn.disabled = false;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('hash', hash);

    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      if (result.status === 'uploaded') {
        responseMessage.textContent = '✅ File uploaded successfully!';
        responseMessage.style.color = 'green';
      } else if (result.status === 'duplicate') {
        responseMessage.textContent = '⚠️ File already uploaded (duplicate)';
        responseMessage.style.color = 'orange';
      } else {
        responseMessage.textContent = '❌ Upload failed: ' + result.message;
        responseMessage.style.color = 'red';
      }
    } catch (err) {
      responseMessage.textContent = '❌ Error uploading file.';
      responseMessage.style.color = 'red';
      console.error(err);
    }
  });
});
