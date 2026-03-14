// Service Worker для кэширования и оффлайн функциональности

const CACHE_NAME = "weather-app-v1";
const STATIC_ASSETS = [
  "/portfolio/",
  "/portfolio/index.html",
  "/portfolio/manifest.json",
];

// Установка Service Worker
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS).catch((error) => {
        console.log("Cache addAll error:", error);
        // Если кэширование не удалось, продолжаем работу
      });
    }),
  );
  self.skipWaiting();
});

// Активация Service Worker
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        }),
      );
    }),
  );
  self.clients.claim();
});

// Обработка fetch запросов (сетевой кэш)
self.addEventListener("fetch", (event) => {
  const { request } = event;

  // Игнорируем не-GET запросы
  if (request.method !== "GET") {
    return;
  }

  // Стратегия для API запросов - сначала сеть
  if (
    request.url.includes("workers.dev") ||
    request.url.includes("openweathermap")
  ) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // Кэшируем успешные API ответы
          if (response && response.status === 200) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(request, clone);
            });
          }
          return response;
        })
        .catch(() => {
          // Если нет сети, возвращаем кэшированный ответ
          return caches.match(request);
        }),
    );
    return;
  }

  // Стратегия для статических ресурсов - кэш сначала
  event.respondWith(
    caches.match(request).then((response) => {
      if (response) {
        return response;
      }
      return fetch(request)
        .then((response) => {
          // Не кэшируем не-успешные ответы
          if (
            !response ||
            response.status !== 200 ||
            response.type === "error"
          ) {
            return response;
          }
          // Кэшируем успешные ответы
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, clone);
          });
          return response;
        })
        .catch(() => {
          // Оффлайн фолбэк
          return caches.match(request);
        });
    }),
  );
});
