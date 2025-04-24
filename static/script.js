document.getElementById('uploadForm').addEventListener('submit', function(event) {
  event.preventDefault();
  
  const fileInput = document.getElementById('fileInput');
  if (!fileInput.files.length) {
    alert("Please select a file to upload.");
    return;
  }

  const file = fileInput.files[0];
  const reader = new FileReader();

  reader.onloadend = function() {
    const wordArray = CryptoJS.lib.WordArray.create(reader.result);
    const hash = CryptoJS.SHA256(wordArray).toString(CryptoJS.enc.Base64);

    document.getElementById('displayHash').innerText = hash;
    const copyBtn = document.getElementById('copyHashBtn');
    copyBtn.disabled = false;
    copyBtn.onclick = () => {
      navigator.clipboard.writeText(hash)
        .then(() => alert('Hash copied to clipboard!'))
        .catch(err => alert('Failed to copy hash.'));
    };

    const formData = new FormData();
    formData.append('file', file);
    formData.append('hash', hash);

    fetch('http://127.0.0.1:5000/upload', {
      method: 'POST',
      body: formData,
    })
    .then(res => res.json())
    .then(data => {
      const msgEl = document.getElementById('responseMessage');
      if (data.status === 'uploaded') {
        msgEl.innerHTML = `<span style="color: green;">${data.message}</span>`;
      } else if (data.status === 'duplicate') {
        msgEl.innerHTML = `<span style="color: orange;">${data.message}</span>`;
      } else {
        msgEl.innerHTML = `<span style="color: red;">${data.message}</span>`;
      }
      fileInput.value = '';
    })
    .catch(() => {
      document.getElementById('responseMessage').innerHTML =
        `<span style="color: red;">Error uploading file</span>`;
    });
  };

  reader.readAsArrayBuffer(file);
});

document.getElementById('checkHashButton').addEventListener('click', function () {
  const hash = document.getElementById('hashInput').value.trim();
  const statusEl = document.getElementById('fileStatus');

  if (!hash) {
    statusEl.innerText = 'Please enter a valid hash.';
    return;
  }

  fetch(`http://127.0.0.1:5000/check?hash=${encodeURIComponent(hash)}`)
    .then(response => {
      if (response.status === 404) {
        statusEl.innerText = 'File not found!';
      } else {
        return response.json();
      }
    })
    .then(data => {
      if (data) {
        statusEl.innerText = `File found: ${data.message}`;
      }
    })
    .catch(() => {
      statusEl.innerText = 'Error checking file status.';
    });
});
