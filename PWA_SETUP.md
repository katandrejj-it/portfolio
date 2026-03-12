# PWA Setup Guide - Погода

## ✅ Что было сделано

Ваш проект "Погода" успешно преобразован в Progressive Web App (PWA). Вот список всех добавленных файлов и изменений:

### 1. **manifest.json** ✓

Манифест PWA приложения с настройками:

- **name**: "Погода" — полное название приложения
- **short_name**: "Погода" — короткое имя для домашнего экрана
- **display**: "standalone" — приложение открывается как отдельное приложение
- **start_url**: "/portfolio/" — стартовая страница (для GitHub Pages)
- **theme_color**: "#0f1729" — цвет темы из вашего дизайна
- **background_color**: "#0f1729" — цвет фона при загрузке

**Иконки:**

- icon-192.png / icon-192-maskable.png (192x192px)
- icon-512.png / icon-512-maskable.png (512x512px)
- screenshot-540x720.png (скриншот приложения)

### 2. **sw.js** ✓

Service Worker с функциональностью:

- ✅ Кэширование статических ресурсов
- ✅ Оффлайн поддержка
- ✅ Умное кэширование API запросов (сетевой кэш)
- ✅ Автоматическое удаление старых версий кэша

### 3. **index.html** ✓ (обновлено)

Добавлены:

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

<!-- Service Worker Registration -->
<script>
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker
        .register("sw.js")
        .then((registration) => console.log("SW registered", registration))
        .catch((error) => console.log("SW registration failed", error));
    });
  }
</script>
```

### 4. **Иконки** ✓

Созданы 5 файлов PNG:

- `icon-192.png` — стандартная иконка 192x192
- `icon-192-maskable.png` — адаптивная иконка для Android
- `icon-512.png` — иконка 512x512
- `icon-512-maskable.png` — адаптивная иконка 512x512
- `screenshot-540x720.png` — скриншот приложения

### 5. **Скрипты генерации** (опционально)

- `generate-pwa-icons.py` — для переиспользования иконок
- `generate-icons.js` — альтернативный способ (требует `sharp`)
- `create-dummy-icons.js` — создание заглушек

---

## 🚀 Как установить приложение

### На Android:

1. Откройте приложение в Chrome/Firefox
2. нажмите ⋮ (меню)
3. Выберите "Установить приложение" или "Add to Home Screen"
4. Приложение появится на домашнем экране

### На iOS 12.2+:

1. Откройте приложение в Safari
2. Нажмите кнопку "Поделиться" (↑)
3. Выберите "На экран \"Домой\""
4. Приложение добавится на домашний экран

### На Windows/macOS:

1. Откройте приложение в Chrome/Edge
2. В адресной строке будет иконка установки
3. Нажмите "Установить"

---

## 📋 Проверка работоспособности

Убедитесь, что всё работает:

1. **Откройте DevTools** (F12 / Cmd+Option+I)
2. **Перейдите на вкладку "Application"**
3. Проверьте:
   - ✅ Manifest файл загружается без ошибок
   - ✅ Service Worker активен и работает
   - ✅ Кэш содержит загруженные ресурсы
   - ✅ Иконки отображаются правильно

### Команды для проверки в консоли:

```javascript
// Проверка регистрации Service Worker
navigator.serviceWorker
  .getRegistrations()
  .then((registrations) => console.log("SW registrations:", registrations));

// Проверка кэша
caches.keys().then((names) => console.log("Caches:", names));

// Проверка манифеста
fetch("manifest.json")
  .then((r) => r.json())
  .then((d) => console.log(d));
```

---

## 🔧 Оптимизация иконок

**Текущие иконки** - это простые заглушки с солнцем и облаком.

Для более красивых иконок используйте:

### 1. **Favicon Generator** (рекомендуется)

- https://www.favicon-generator.org/
- Загрузите PNG или SVG
- Скачайте пакет иконок разных размеров
- Замените существующие файлы

### 2. **PWA Builder** (комплексное решение)

- https://www.pwabuilder.com/
- Поддерживает создание иконок и манифеста
- Автоматическая генерация иконок для всех платформ

### 3. **Figma** (для дизайнеров)

- Экспортируйте PNG в разных размерах
- Оптимизируйте через TinyPNG

---

## 🌐 Параметры GitHub Pages

Файл [manifest.json](manifest.json) уже настроен для GitHub Pages:

```json
{
  "start_url": "/portfolio/",
  "scope": "/portfolio/"
}
```

Эти пути соответствуют структуре: `username.github.io/portfolio/`

**Если ваш репозиторий имеет другое имя**, обновите `start_url` и `scope` в manifest.json:

- Замените `portfolio` на название вашего репозитория

---

## ✨ Проверка взаимодействия с Cloudflare Worker

Ваше приложение продолжит работать с Cloudflare Worker:

✅ **API запрос остаётся прежним:**

```javascript
const response = await fetch(
  `https://rapid-sun-74ab.katandrejj.workers.dev/?city=${encodeURIComponent(city)}`,
);
```

✅ **Service Worker не прерывает работу:**

- Сетевые запросы к API имеют приоритет
- Результаты кэшируются для оффлайн доступа
- Инструкция `fetch` обрабатывает сетевые ошибки

✅ **Оффлайн функциональность:**

- При наличии интернета - актуальная погода
- При отсутствии - показываются закэшированные данные

---

## 📱 Внешний вид приложения

### На домашнем экране:

- Иконка: солнце + облако (темный фон #0f1729)
- Название: "Погода"
- Сплэш-экран при запуске с вашим цветом темы

### При открытии:

- Полноэкранное приложение без адресной строки
- Темная тема (как настроено в `data-theme="night"`)
- iOS вверху отобразит статус-бар

---

## 🚨 Возможные проблемы

### 1. Приложение не устанавливается

- Убедитесь, что сайт на **HTTPS** (PWA требует HTTPS)
- Проверьте браузер - PWA поддерживается в Chrome/Firefox/Safari
- На iOS требуется Safari 12.2+

### 2. Иконка не отображается

- Проверьте пути в manifest.json - они должны быть абсолютными или относительными от корня
- Убедитесь, что файлы иконок загружены в репозиторий
- Очистите кэш браузера (Ctrl+Shift+Delete)

### 3. Service Worker не регистрируется

- Должен быть на **HTTPS**
- Откройте DevTools > Application > Service Workers
- Проверьте консоль на ошибки

### 4. Работает только на HTTPS

- Локально работает на `http://localhost`
- На production требуется HTTPS сертификат

---

## 📚 Дополнительные ресурсы

- [MDN - Progressive Web Apps](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
- [Google - Web App Manifest](https://web.dev/add-manifest/)
- [Service Workers Specification](https://w3c.github.io/ServiceWorker/)
- [PWA Checklist](https://web.dev/pwa-checklist/)

---

## 🎉 Готово к развёртыванию!

Ваш проект готов к использованию как PWA. Просто:

1. ✅ Залейте файлы на GitHub Pages
2. ✅ Откройте сайт по HTTPS
3. ✅ Приложение будет установляемым на мобильных устройствах

**Успехов! 🚀**
