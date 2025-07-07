document.addEventListener("DOMContentLoaded", () => {
  // 0) Локальное время
  document.querySelectorAll(".uploaded-at").forEach(td => {
    const utcSec = parseInt(td.dataset.utc, 10);
    // создаём объект Date в UTC
    const dt = new Date(utcSec * 1000);
    // выводим в локальном формате пользователя
    td.textContent = dt.toLocaleString();
  });

  // 1) Одиночное скачивание
  document.querySelectorAll(".dl-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const name = btn.dataset.name;
      const a = document.createElement("a");
      a.href     = `/images/${encodeURIComponent(name)}`;
      a.download = name;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    });
  });

  // 2) «Выбрать всё»
  const downloadBtn = document.getElementById("downloadSelectedBtn");
  const deleteBtn   = document.getElementById("deleteSelectedBtn");
  const checkboxes  = Array.from(document.querySelectorAll(".row-checkbox"));
  const selectAll   = document.getElementById("selectAll");
  const form        = document.getElementById("multiDeleteForm");

  function updateActionBtns() {
    const any = checkboxes.some(cb => cb.checked);
    downloadBtn.disabled = !any;
    deleteBtn.disabled   = !any;
  }


  selectAll.addEventListener("change", () => {
    checkboxes.forEach(cb => cb.checked = selectAll.checked);
    updateActionBtns();
  });

  // Отдельные чекбоксы
  checkboxes.forEach(cb => {
    cb.addEventListener("change", () => {
      if (!cb.checked) selectAll.checked = false;
      updateActionBtns();
    });
  });

  // 2a) Кнопка Скачать выбранное
  downloadBtn.addEventListener("click", () => {
    checkboxes
      .filter(cb => cb.checked)
      .forEach(cb => {
        const name = cb.value;
        const a = document.createElement("a");
        a.href     = `/images/${encodeURIComponent(name)}`;
        a.download = name;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      });
  });

  // 2b) Кнопка Удалить выбранное
  form.addEventListener("submit", async e => {
    e.preventDefault();
    if (!confirm("Удалить отмеченные файлы?")) return;
    const toDelete = checkboxes.filter(cb => cb.checked).map(cb => cb.value);
    try {
      await Promise.all(toDelete.map(name =>
        fetch(`/images/delete/${encodeURIComponent(name)}`, {
          method: 'DELETE',
          credentials: 'same-origin'
        })
      ));
      location.reload();
    } catch (err) {
      alert("Ошибка при удалении: " + err.message);
    }
  });

  // 3) Кнопка Удалить
  document.querySelectorAll(".del-btn").forEach(btn => {
    btn.addEventListener("click", async () => {
      const name = btn.dataset.name;
      if (!confirm(`Удалить ${name}?`)) return;
      try {
        await fetch(`/images/delete/${encodeURIComponent(name)}`, {
          method: "DELETE",
          credentials: "same-origin"
        });
        location.reload();
      } catch (err) {
        alert("Ошибка при удалении: " + err.message);
      }
    });
  });

  // 4) Прокрутка таблицы
  const tableContainer = document.querySelector('.table-container');
  if (tableContainer) {
    let scrollTimeout = null;
    tableContainer.addEventListener('scroll', () => {
      tableContainer.classList.add('scrolling');
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(() => {
        tableContainer.classList.remove('scrolling');
      }, 800);
    });
  }
});
