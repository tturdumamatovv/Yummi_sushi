document.addEventListener("DOMContentLoaded", function () {
  let notificationSocket;
  let modalCount = 0;

  // Создаем аудио объект
  const audioElement = new Audio("/static/audio/notification.mp3");

  function connectWebSocket() {
    const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";
    const wsUrl = `${protocol}${window.location.host}/ws/notification/`;

    notificationSocket = new WebSocket(wsUrl);

    notificationSocket.onopen = function (e) {
      console.log("Соединение с WebSocket установлено");
    };

    notificationSocket.onmessage = function (e) {
      console.log("Получено сообщение через WebSocket:", e.data);
      try {
        const data = JSON.parse(e.data);
        showOrderNotification(data.message);
        playNotificationSound();
      } catch (error) {
        console.error("Ошибка при разборе данных:", error);
      }
    };

    notificationSocket.onclose = function (e) {
      console.log("Соединение с WebSocket закрыто. Попытка переподключения...");
      setTimeout(connectWebSocket, 5000);
    };

    notificationSocket.onerror = function (err) {
      console.error("Ошибка WebSocket:", err);
      notificationSocket.close();
    };
  }

  function playNotificationSound() {
    audioElement.play().catch(error => {
      console.error("Ошибка воспроизведения звука:", error);
    });
  }

  function showOrderNotification(message) {
    console.log("Попытка показать уведомление:", message);
    const modalId = `orderModal${Date.now()}`;
    modalCount++;

    const modalHtml = `
      <div id="${modalId}" class="custom-modal">
        <div class="custom-modal-content">
          <div class="custom-modal-header">
            <span class="custom-modal-title">Уведомление о заказе</span>
            <span class="custom-modal-close">&times;</span>
          </div>
          <div class="custom-modal-body">
            <p>${message}</p>
          </div>
          <div class="custom-modal-footer">
            <button class="custom-btn custom-btn-secondary" data-action="close">Закрыть</button>
            <a href="/admin/orders/order/" class="custom-btn custom-btn-primary">Перейти к заказам</a>
          </div>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML("beforeend", modalHtml);

    const modalElement = document.getElementById(modalId);
    if (!modalElement) {
      console.error("Не удалось найти элемент модального окна");
      return;
    }

    modalElement.style.display = "block";

    // Применяем каскадное расположение
    const modalContent = modalElement.querySelector(".custom-modal-content");
    modalContent.style.transform = `translate(${modalCount * 10}px, ${
      modalCount * 10
    }px)`;

    const closeModal = () => {
      modalElement.style.display = "none";
      modalElement.remove();
      modalCount--;
    };

    modalElement
      .querySelector(".custom-modal-close")
      .addEventListener("click", closeModal);
    modalElement
      .querySelector('[data-action="close"]')
      .addEventListener("click", closeModal);

    modalElement.addEventListener("click", event => {
      if (event.target === modalElement) {
        closeModal();
      }
    });
  }

  // Проверяем, находимся ли мы в административной панели
  if (window.location.pathname.startsWith("/admin/")) {
    console.log("Инициализация WebSocket для админ-панели");
    connectWebSocket();
  } else {
    console.log("Не в админ-панели, WebSocket не инициализирован");
  }
});
