document.addEventListener('DOMContentLoaded', () => {
    const preloader = document.getElementById('preloader');
    const content = document.getElementById('content');

    // Скроет анимацию и покажет основной контент через задержку после полной загрузки
    window.addEventListener('load', () => {
        setTimeout(() => {
            preloader.style.opacity = '0';
            setTimeout(() => {
                preloader.style.display = 'none';
                content.style.display = 'block';
            }, 500); // Задержка для плавного исчезновения
        }, 3000); // Время задержки для предзагрузчика (в миллисекундах)
    });
});
