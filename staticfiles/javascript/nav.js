document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navList = document.querySelector('.nav-list');

    menuToggle.addEventListener('click', function() {
        navList.classList.toggle('active');
    });

    // Cerrar el menú al hacer clic fuera de él
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.nav-menu')) {
            navList.classList.remove('active');
        }
    });
});