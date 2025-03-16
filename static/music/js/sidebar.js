document.addEventListener('DOMContentLoaded', function() {
  // Получаем элементы
  const menuToggle = document.getElementById('menu-toggle');
  const sidebar = document.getElementById('sidebar');
  const closeBtn = document.getElementById('close-menu');
  const backdrop = document.getElementById('sidebar-backdrop');

  // Функция для открытия меню
    function openSidebar() {
      sidebar.classList.add('active');
      backdrop.classList.add('active');
      menuToggle.classList.add('active');
      // Скрываем кнопку-гамбургер и программно, для надежности
      menuToggle.style.visibility = 'hidden';
      document.body.style.overflow = 'hidden'; // Запрещаем прокрутку страницы
    }

    // Функция для закрытия меню (исправленная)
    function closeSidebar() {
      sidebar.classList.remove('active');
      backdrop.classList.remove('active');
      menuToggle.classList.remove('active');
      // Показываем кнопку-гамбургер снова
      menuToggle.style.visibility = 'visible';
      document.body.style.overflow = ''; // Разрешаем прокрутку страницы
    }

  // Обработчики событий
  menuToggle.addEventListener('click', openSidebar);
  closeBtn.addEventListener('click', closeSidebar);
  backdrop.addEventListener('click', closeSidebar);

  // Закрытие меню при переходе по ссылке
  const navLinks = document.querySelectorAll('.nav-link');
  navLinks.forEach(link => {
    link.addEventListener('click', function() {
      if (window.innerWidth <= 768) {
        closeSidebar();
      }
    });
  });

  // Проверка размера экрана при изменении
  window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
      closeSidebar();
    }
  });

  // Добавляем свайп для закрытия меню на мобильных устройствах
  let touchStartX = 0;
  let touchEndX = 0;

  sidebar.addEventListener('touchstart', function(e) {
    touchStartX = e.changedTouches[0].screenX;
  }, false);

  sidebar.addEventListener('touchend', function(e) {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
  }, false);

  function handleSwipe() {
    // Свайп влево для закрытия меню
    if (touchStartX - touchEndX > 50 && window.innerWidth <= 768) {
      closeSidebar();
    }
  }
});