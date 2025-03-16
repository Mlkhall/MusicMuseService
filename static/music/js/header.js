document.addEventListener('DOMContentLoaded', function() {
  const searchForm = document.getElementById('search-form');
  const searchInput = document.getElementById('search-input');
  const clearSearch = document.getElementById('clear-search');

  // Очистка поля поиска
  if (clearSearch) {
    clearSearch.addEventListener('click', function() {
      searchInput.value = '';
      searchInput.focus();
    });
  }

  // Предотвращаем отправку пустой формы
  if (searchForm) {
    searchForm.addEventListener('submit', function(e) {
      if (!searchInput.value.trim()) {
        e.preventDefault();
        searchInput.focus();

        // Добавляем анимацию встряхивания при попытке отправить пустую форму
        searchInput.classList.add('shake-animation');
        setTimeout(() => {
          searchInput.classList.remove('shake-animation');
        }, 500);
      }
    });
  }

  // Анимация при фокусе
  if (searchInput) {
    searchInput.addEventListener('focus', function() {
      this.parentElement.classList.add('focused');
    });

    searchInput.addEventListener('blur', function() {
      this.parentElement.classList.remove('focused');
    });
  }
});
