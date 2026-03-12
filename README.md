🌦️ Telegram Weather Mini App (Fullstack)
Telegram Mini App для получения погоды в реальном времени. Проект демонстрирует навыки создания современных веб-интерфейсов и безопасной работы с серверной логикой.

🚀 Технологический стек:
Frontend: HTML5, JavaScript (ES6+), Tailwind CSS, DaisyUI.

Backend: Cloudflare Workers (Runtime: V8).

API: Telegram Web Apps SDK, OpenWeatherMap API.

DevOps: GitHub Pages (хостинг фронтенда), Cloudflare (Serverless бэкенд).

💡 Ключевые особенности:
Serverless Архитектура: Бэкенд реализован на Cloudflare Workers, что обеспечивает мгновенный отклик и отсутствие затрат на сервер.

Безопасность: Реализован Proxy-сервер на стороне Воркера для защиты API-ключей. Ключи не «светятся» в исходном коде фронтенда и хранятся в Environment Variables.

CORS & OPTIONS: Настроены политики безопасности для взаимодействия между доменами GitHub и Cloudflare.

UX/UI: Адаптивный дизайн с поддержкой ночной темы, индикация загрузки и использование Telegram Haptic Feedback (виброотклик).

🛠 Как это работает:
Пользователь вводит город в Telegram Web App.

Фронтенд отправляет запрос на Cloudflare Worker.

Воркер извлекает секретный API-ключ, запрашивает данные у OpenWeatherMap и возвращает их фронтенду.

Данные отображаются в интерфейсе с использованием Telegram SDK.
