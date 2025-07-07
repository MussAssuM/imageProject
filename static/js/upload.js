const dropzone       = document.getElementById('dropzone');
const dropzonePrimary = document.getElementById('dropzonePrimary');
const dropzoneMessage = document.getElementById('dropzoneMessage');
const fileInput      = document.getElementById('fileInput');
const previewBox     = document.getElementById('previewBox');
const uploadForm     = document.getElementById('uploadForm');
const loadingOverlay = document.getElementById("loadingOverlay");

dropzone.addEventListener('dragover', e => {
    e.preventDefault();
    dropzone.classList.add('hover');
});
dropzone.addEventListener('dragleave', e => dropzone.classList.remove('hover'));
dropzone.addEventListener('drop', e => dropzone.classList.remove('hover'));

fileInput.addEventListener('change', e => {
    // Скрываем индикатор загрузки, если он был ранее показан
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (loadingOverlay) {
        loadingOverlay.style.display = 'none';
    }

    // Очищаем контейнер превью и прячем сообщение в drop-zone
    previewBox.innerHTML = "";
    if (dropzoneMessage) {
        dropzoneMessage.style.display = "none";
    }

    // Если файл выбран – сбрасываем возможные предупреждения drop-zone
    if (fileInput.files.length > 0) {
        dropzonePrimary.textContent = "Select a file or drag & drop here";
        dropzonePrimary.style.color = "";
    }

    const file = e.target.files[0];
    if (!file) {
        // Если файла нет, убеждаемся, что сообщение видно
        dropzoneMessage.style.display = "block";
        return;
    }

    // Проверка размера файла для клиентской стороны (максимум 5 MB)
    const maxSizeInBytes = 5 * 1024 * 1024;
    if (file.size > maxSizeInBytes) {
        alert("Файл превышает допустимый размер (5 MB)");
        fileInput.value = "";  // Сбрасываем выбранный файл
        dropzoneMessage.style.display = "block"; // Возвращаем сообщение
        return
    }

    // Проверка типа файла (допустим только JPG, PNG и GIF)
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
    if (!allowedTypes.includes(file.type)) {
        alert("Неверный формат файла. Допустимые форматы: JPG, PNG, GIF");
        fileInput.value = "";  // сбрасываем выбранный файл
        dropzoneMessage.style.display = "block"; // Возвращаем сообщение
        return;
    }

    // Если файл прошёл валидацию, создаём превью изображения
    const img = document.createElement('img');
    img.src = URL.createObjectURL(file);
    img.onload = () => URL.revokeObjectURL(img.src);
    previewBox.appendChild(img);
});

uploadForm.addEventListener('submit', e => {
    if (!fileInput.files.length) {
        e.preventDefault();
        dropzonePrimary.textContent = "Сначала выберите файл!";
        dropzonePrimary.style.color = "red";
    } else {
        loadingOverlay.style.display = "flex";
    }
});

document.addEventListener('click', evt => {
    if (evt.target.id === 'copyBtn') {
        navigator.clipboard.writeText(document.getElementById('fileUrl').value);
        evt.target.textContent = 'COPIED!';
        setTimeout(() => evt.target.textContent = 'COPY', 1500);
    }
});

document.addEventListener("DOMContentLoaded", () => {
  const fileUrlElem = document.getElementById("fileUrl");
  const rel = fileUrlElem.value;
  if (rel.startsWith("/")) {
    fileUrlElem.value = `${window.location.origin}${rel}`;
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const toast = document.getElementById("successToast");
  if (!toast) return;
  if (toast.classList.contains("hidden")) {
    toast.classList.remove("hidden");
    requestAnimationFrame(() => {
      toast.classList.add("visible");
    });
    setTimeout(() => {
      toast.classList.remove("visible");
      setTimeout(() => toast.classList.add("hidden"), 500);
    }, 3000);
  }
});