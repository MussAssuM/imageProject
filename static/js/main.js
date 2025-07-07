// static/js/main.js

document.addEventListener('DOMContentLoaded', () => {
  // 1. Переключение активного таба (кликом по навигации)
  const tabs = document.querySelectorAll('nav .tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
    });
  });

  // 2. Скрываем оверлей загрузки, если он есть на странице
  const overlay = document.getElementById('loadingOverlay');
  if (overlay) {
    overlay.style.display = 'none';
  }
});