document.addEventListener('DOMContentLoaded', function () {
    const chatApp = document.getElementById('chat-app');
    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('chat-message-input');
    const messageSubmit = document.getElementById('chat-message-submit');
    const autoScrollCheckbox = document.getElementById('auto-scroll-checkbox');
    const ordersList = document.getElementById('orders');
    const ordersContainer = document.getElementById('orders-list');
    const ordersLoading = document.getElementById('orders-loading');
    let ws = null;

    function closeWebSocket() {
        if (ws) {
            ws.close();
            console.log('Closing existing WebSocket connection.');
        }
    }

    function openChat(roomId, userId, userName) {
        closeWebSocket(); // Закрываем предыдущее соединение

        const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        const wsUrl = `${protocol}${window.location.host}/ws/chat/${roomId}/`;
        ws = new WebSocket(wsUrl);

        ws.onopen = () => console.log(`WebSocket connection established to room ${roomId}`);
        ws.onerror = error => console.error('WebSocket error:', error);
        ws.onmessage = event => displayMessage(JSON.parse(event.data));
        ws.onclose = () => console.log('WebSocket connection closed');

        // Очищаем старые сообщения и заказы
        chatMessages.innerHTML = '';
        ordersList.innerHTML = '';
        document.getElementById('chat-room-title').textContent = `Административный Чат ${roomId}`;
        chatApp.style.display = 'block';
        ordersContainer.style.display = 'block';

        // Загружаем сообщения чата и заказы
        loadMessages(roomId);
        loadOrders(userId);
    }

    function loadMessages(roomId) {
        console.log(`Loading messages for room ${roomId}`);
        const spinner = document.getElementById('loading-spinner');
        spinner.style.display = 'block';

        fetch(`/support/api/messages/${roomId}/`)
            .then(response => response.json())
            .then(data => {
                chatMessages.innerHTML = ''; // Очищаем перед загрузкой

                if (data.messages && Array.isArray(data.messages)) {
                    data.messages.forEach(message => {
                        displayMessage({
                            sender_id: message.sender,
                            sender_username: message.sender_phone,
                            message: message.message,
                            timestamp: message.timestamp
                        });
                    });
                } else {
                    console.error('Data does not contain expected "messages" array:', data);
                }
            })
            .catch(error => console.error('Error loading messages:', error))
            .finally(() => {
                spinner.style.display = 'none';
                // Всегда прокручиваем вниз после загрузки сообщений
                scrollToBottom(true);
            });
    }

    function displayMessage(data) {
        console.log(data,'new message')
        const messageElement = document.createElement('li');
        const userId = document.body.getAttribute('data-user-id');

        // Определяем стиль сообщения
        const messageClass = data.sender_id == userId ? 'user-message' : 'other-message';
        messageElement.classList.add('list-group-item', messageClass);

        // Форматируем сообщение для отображения
        messageElement.innerHTML = `<strong>${data.sender_username}:</strong> ${data.message} <br> <small>${new Date(data.timestamp).toLocaleString()}</small>`;

        // Добавляем сообщение в чат
        chatMessages.appendChild(messageElement);

        // Прокручиваем вниз, если включена автопрокрутка
        if (autoScrollCheckbox.checked) {
            scrollToBottom();
        }
    }

    function scrollToBottom(force = true) {
        // Прокручиваем вниз всегда при force=true (например, после загрузки сообщений)
        // Или если автопрокрутка включена
        if (force || autoScrollCheckbox.checked) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

function loadOrders(userId) {
    ordersLoading.style.display = 'block';

    fetch(`/support/api/orders/${userId}/`)
        .then(response => response.json())
        .then(data => {
            ordersLoading.style.display = 'none';
            if (data.orders && Array.isArray(data.orders)) {
                data.orders.forEach(order => {
                    // Создаем элемент ссылки
                    const orderElement = document.createElement('li');
                    const linkElement = document.createElement('a');
                    linkElement.href = `/admin/orders/order/${order.id}/change/`; // Ссылка на детали заказа
                    linkElement.textContent = `Заказ №${order.id}: ${getStatusText(order.order_status)}`;

                    // Применяем цвет в зависимости от статуса
                    linkElement.style.color = getStatusColor(order.order_status);

                    // Добавляем ссылку в элемент списка
                    orderElement.appendChild(linkElement);
                    ordersList.appendChild(orderElement);
                });
            }
        })
        .catch(error => {
            ordersLoading.style.display = 'none';
            console.error('Error loading orders:', error);
        });
}

// Функция для получения текста статуса
function getStatusText(status) {
    const statusMap = {
        'pending': 'В ожидании',
        'in_progress': 'В процессе',
        'delivery': 'Доставка',
        'completed': 'Завершено',
        'cancelled': 'Отменено'
    };
    return statusMap[status] || 'Неизвестно';
}

// Функция для получения цвета в зависимости от статуса
function getStatusColor(status) {
    const colorMap = {
        'pending': 'orange',      // В ожидании
        'in_progress': 'blue',    // В процессе
        'delivery': 'purple',     // Доставка
        'completed': 'green',     // Завершено
        'cancelled': 'red'        // Отменено
    };
    return colorMap[status] || 'black'; // По умолчанию черный цвет
}
    // Обработка кликов на список чатов
    document.querySelectorAll('.chat-link').forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            const roomId = this.getAttribute('data-room-id');
            const userId = this.getAttribute('data-user-id');
            openChat(roomId, userId);
        });
    });

    // Отправка сообщения
    messageSubmit.addEventListener('click', function (event) {
        event.preventDefault();
        const message = messageInput.value.trim();
        if (message && ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                message: message,
                sender_id: document.body.getAttribute('data-user-id'),
                sender_username: document.body.getAttribute('data-user-username')
            }));
            messageInput.value = ''; // Очищаем поле ввода после отправки
        }
    });
});
