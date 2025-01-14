 function redirectToProfilePage() {
            const userId = localStorage.getItem("userId");
            if (userId) {
                window.location.href = `/pages/profile/${userId}`;
            } else {
                console.error("Telegram ID не найден в localStorage.");
                alert("Telegram ID не найден. Пожалуйста, перезагрузите страницу.");
            }
        }

  function redirectToWalletPage() {
            const userId = localStorage.getItem("userId");
            if (userId) {
                window.location.href = `/pages/wallet/${userId}`;
            } else {
                console.error("Telegram ID не найден в localStorage.");
                alert("Telegram ID не найден. Пожалуйста, перезагрузите страницу.");
            }
        }

function redirectToPortfolioPage() {
    const userId = localStorage.getItem("userId");
    if (userId) {
        window.location.href = `/pages/portfolio_page?tg_id=${userId}`;
    } else {
        console.error("Telegram ID не найден в localStorage.");
        alert("Telegram ID не найден. Пожалуйста, перезагрузите страницу.");
    }
}


function redirectToCurrentEventPage(event_id) {
    const userId = localStorage.getItem("userId");
    if (userId) {
        window.location.href = `/pages/event_by_id?tg_id=${userId}&event_id=${event_id}`;
    } else {
        console.error("Telegram ID не найден в localStorage.");
        alert("Telegram ID не найден. Пожалуйста, перезагрузите страницу.");
    }
}




