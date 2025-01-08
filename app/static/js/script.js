document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelector('.slides');
    const slide = document.querySelectorAll('.slide');
    const next = document.querySelector('.next');
    const prev = document.querySelector('.prev');
    let currentIndex = 0;
    const interval = 5500; // Интервал в миллисекундах для автоматического переключения

    // Функция для обновления слайдера
    function updateSlider() {
        slides.style.transform = `translateX(-${currentIndex * 100}%)`;
    }

    // Функция для перехода к следующему слайду
    function nextSlide() {
        currentIndex = (currentIndex + 1) % slide.length;
        updateSlider();
    }

    // Функция для перехода к предыдущему слайду
    function prevSlide() {
        currentIndex = (currentIndex - 1 + slide.length) % slide.length;
        updateSlider();
    }

    // Слушатели событий для кнопок
    next.addEventListener('click', () => {
        nextSlide();
        resetAutoSlide(); // Сброс таймера автопереключения
    });

    prev.addEventListener('click', () => {
        prevSlide();
        resetAutoSlide(); // Сброс таймера автопереключения
    });

    // Автоматическое переключение слайдов
    let autoSlide = setInterval(nextSlide, interval);

    // Функция сброса таймера автопереключения
    function resetAutoSlide() {
        clearInterval(autoSlide); // Останавливаем текущее автопереключение
        autoSlide = setInterval(nextSlide, interval); // Перезапускаем автопереключение
    }
});
