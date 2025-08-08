        document.getElementById('input-image').addEventListener('change', async (event) => {
            const formData = new FormData();
            formData.append('image', event.target.files[0]);
            const response = await fetch('/detect-image', { method: 'POST', body: formData });
            const data = await response.json();

            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';  
            resultDiv.innerHTML = ''; 

            const img = document.createElement('img');
            img.src = data.result;
            img.alt = "Processed Image";
            img.className = "img-fluid";
            img.style.maxWidth = "640px";
            img.style.maxHeight = "400px";

            resultDiv.appendChild(img);
        });

document.getElementById('input-video').addEventListener('change', async (event) => {
  const file = event.target.files[0];

  const formData = new FormData();
  formData.append('video', file);

  const response = await fetch('/detect-video', {
    method: 'POST',
    body: formData,
  });

  const data = await response.json();

  const container = document.getElementById('result');
  container.style.display = 'block';
  container.innerHTML = ''; 

  const video = document.createElement('video');
  video.controls = true;
  video.style.maxWidth = '640px';
  video.style.maxHeight = '400px';
  video.src = data.result; 
  video.load();
  container.appendChild(video);

});