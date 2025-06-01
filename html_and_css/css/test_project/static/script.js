const fileInput = document.getElementById('fileInput');
const progressBar = document.getElementById('progressBar');
const timeDisplay = document.getElementById('timeRemaining');

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  if (!file) return;

  const xhr = new XMLHttpRequest();
  const formData = new FormData();
  formData.append('file', file);

  const startTime = Date.now();

  xhr.upload.onprogress = (event) => {
    if (event.lengthComputable) {
      const uploaded = event.loaded;
      const total = event.total;
      const percent = (uploaded / total) * 100;

      progressBar.style.width = percent + '%';
      progressBar.textContent = Math.round(percent) + '%';

      const elapsed = (Date.now() - startTime) / 1000;
      const speed = uploaded / elapsed;
      const remaining = (total - uploaded) / speed;

      timeDisplay.textContent = `Estimated time left: ${Math.round(remaining)}s`;
    }
  };

  xhr.onload = () => {
    timeDisplay.textContent = "Upload complete!";
  };

  xhr.onerror = () => {
    timeDisplay.textContent = "Upload failed.";
  };

  xhr.open('POST', '/upload');
  xhr.send(formData);
});
