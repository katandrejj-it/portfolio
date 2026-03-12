# PWA Checklist для проекта "Погода"

## ✅ Обязательные файлы

- [x] **manifest.json** — создан с корректными путями для `/portfolio/`
  - name: "Погода"
  - start_url: "/portfolio/"
  - display: "standalone"
  - theme_color: "#0f1729"
  - icons: 4 файла (192, 192-maskable, 512, 512-maskable)

- [x] **sw.js** — Service Worker с функциональностью
  - Кэширование статических ресурсов
  - Поддержка оффлайн режима
  - Сетевой кэш для API

- [x] **index.html обновлён**
  - Ссылка на manifest.json
  - iOS мета-теги (apple-mobile-web-app-capable)
  - Регистрация Service Worker

- [x] **Иконки созданы**
  - icon-192.png ✓
  - icon-192-maskable.png ✓
  - icon-512.png ✓
  - icon-512-maskable.png ✓
  - screenshot-540x720.png ✓

## ✅ Интеграция с существующим кодом

- [x] Cloudflare Worker API — НЕ затронут
  - API URL остаётся: `https://rapid-sun-74ab.katandrejj.workers.dev/?city=...`
  - Service Worker перехватывает fetch и кэширует результаты

- [x] Telegram WebApp — работает как было
  - Все функции (tg.showAlert, HapticFeedback) сохранены
  - Service Worker не интерферирует

- [x] UI/стили (Tailwind + DaisyUI) — изменений нет

## ✅ Тестирование перед развёртыванием

Перед загрузкой на GitHub Pages проверьте:

```bash
# 1. Проверка файлов
ls -la *.json *.js icon-*.png screenshot-*.png

# 2. Валидация manifest.json
cat manifest.json | jq .  # Если установлен jq

# 3. Проверка путей в manifest.json
grep -n "start_url\|scope" manifest.json

# 4. Проверка Service Worker
grep -n "sw.js" index.html

# 5. Проверка иконок
file icon-*.png
```

## 🧪 Локальное тестирование

### Способ 1: Python HTTP сервер

```bash
cd /path/to/portfolio
python3 -m http.server 8000
# Откройте http://localhost:8000
```

### Способ 2: Node.js http-server

```bash
npm install -g http-server
http-server
```

### DevTools проверка:

1. Откройте F12 → Application tab
2. Проверьте:
   - Manifest файл загружается
   - Service Worker активен
   - Cache Storage содержит ресурсы

## 📦 Файловая структура проекта

```
portfolio/
├── index.html          ✅ обновлён (PWA + SW registration)
├── manifest.json       ✅ новый файл (PWA конфигурация)
├── sw.js              ✅ новый файл (Service Worker)
├── icon-192.png       ✅ новый файл (иконка)
├── icon-192-maskable.png  ✅ новый файл
├── icon-512.png       ✅ новый файл
│ icon-512-maskable.png    ✅ новый файл
├── screenshot-540x720.png ✅ новый файл
├── generate-pwa-icons.py  ✅ скрипт опционально
├── generate-icons.js      ✅ скрипт опционально
├── create-dummy-icons.js  ✅ скрипт опционально
├── PWA_SETUP.md           📚 документация
├── README.md              (не изменён)
├── resume.md              (не изменён)
└── .git/                  (не изменён)
```

## 🔍 Что изменилось в index.html?

### Добавлено в `<head>`:

```html
<!-- PWA Manifest -->
<link rel="manifest" href="manifest.json" />

<!-- iOS Meta Tags -->
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta
  name="apple-mobile-web-app-status-bar-style"
  content="black-translucent"
/>
<meta name="apple-mobile-web-app-title" content="Погода" />
<link rel="apple-touch-icon" href="icon-192.png" />
<meta name="theme-color" content="#0f1729" />
```

### Добавлено перед `</body>`:

```html
<!-- Service Worker Registration -->
<script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker
        .register('sw.js')
        .then(...)
        .catch(...);
    });
  }
</script>
```

## ✨ Готовые команды для развёртывания

```bash
# 1. Проверка статуса
git status

# 2. Добавление файлов
git add manifest.json sw.js index.html icon-*.png screenshot-*.png PWA_SETUP.md

# 3. Коммит
git commit -m "feat: add PWA support - manifest.json, Service Worker, app icons"

# 4. Публикация
git push origin main

# 5. GitHub Pages автоматически обновит сайт (~1 минута)
```

## 🎯 Ожидаемый результат

После развёртывания на GitHub Pages:

1. **На мобильном Android (Chrome)**
   - При открытии будет предложение "Установить приложение"
   - Иконка появится на домашнем экране
   - Откроется как полноэкранное приложение

2. **На iPhone/iPad (Safari)**
   - Можно добавить через "Поделиться" → "На экран Домой"
   - Будет использоваться apple-touch-icon
   - Работает с iOS 12.2+

3. **Оффлайн функциональность**
   - Если интернет отключёнкэш предоставляет сохранённые данные
   - API запросы повторяются при восстановлении соединения

## ⚠️ Важное замечание

**На локальном http:// некоторые PWA функции не работают** (требуется HTTPS):

- Service Worker регистрируется, но с ограничениями
- Для полного тестирования используйте `localhost` или GitHub Pages

---

## 📞 Если что-то пошло не так

1. Очистите кэш браузера: Ctrl+Shift+Delete
2. Откройте DevTools (F12) → Application
3. Удалите Service Worker и кэши
4. Перезагрузите страницу (Ctrl+F5)
5. Проверьте консоль на ошибки

---

**Проект "Погода" успешно преобразован в PWA! 🎉**
