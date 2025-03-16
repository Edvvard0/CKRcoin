window.addEventListener('load', (event) => {
    const tg = window.Telegram.WebApp;
    tg.ready(); // Подготовка WebApp
    tg.expand(); // Разворачиваем WebApp
    tg.disableVerticalSwipes();

    // Сохраняем userId в localStorage
    const userId = tg.initDataUnsafe.user?.id;

    if (userId) {
        localStorage.setItem("userId", userId);
        console.log("User ID сохранен:", userId);
    } else {
        console.error("User ID не найден в initDataUnsafe.");
        alert("User ID не найден. Пожалуйста, перезагрузите страницу.");
    }
});


// Перенаправление на другую страницу
 function redirectToMainPage() {
            const userId = localStorage.getItem("userId");
            if (userId) {
                window.location.href = `/pages/main/${userId}`;
            } else {
                console.error("Telegram ID не найден в localStorage.");
                alert("Telegram ID не найден. Пожалуйста, перезагрузите страницу.");
            }
        }