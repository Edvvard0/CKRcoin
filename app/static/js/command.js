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

