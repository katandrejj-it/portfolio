#!/usr/bin/env node

/**
 * Скрипт для генерации иконок PWA
 * Требует установленный Node.js и пакет 'sharp'
 *
 * Установка: npm install sharp
 * Запуск: node generate-icons.js
 */

const fs = require("fs");
const path = require("path");

// Попытаемся использовать sharp, если он установлен
let sharp;
try {
  sharp = require("sharp");
} catch (error) {
  console.log('Пакет "sharp" не установлен.');
  console.log("Установите его командой: npm install sharp");
  console.log("\nАльтернатива: используйте онлайн генератор иконок:");
  console.log("https://www.pwabuilder.com/");
  console.log("или");
  console.log("https://www.favicon-generator.org/");
  process.exit(1);
}

// SVG для погодного приложения (облако с солнцем)
const SVG_ICON = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <!-- Фон -->
  <circle cx="100" cy="100" r="100" fill="#0f1729"/>
  
  <!-- Солнце -->
  <circle cx="60" cy="60" r="30" fill="#FFD700"/>
  
  <!-- Облако -->
  <path d="M 70 100 Q 70 85 85 85 Q 95 75 105 85 Q 120 80 125 95 Q 140 100 140 115 Q 140 130 125 135 L 80 135 Q 70 135 70 125 Z" 
        fill="#E8F4F8" opacity="0.9"/>
  
  <!-- Капли воды -->
  <circle cx="90" cy="125" r="4" fill="#4DA6FF"/>
  <circle cx="105" cy="130" r="4" fill="#4DA6FF"/>
  <circle cx="120" cy="125" r="4" fill="#4DA6FF"/>
</svg>
`;

async function generateIcons() {
  try {
    const outputDir = __dirname;

    console.log("📦 Генерирую иконки PWA...\n");

    // Создаём временный SVG файл
    const svgPath = path.join(outputDir, "temp-icon.svg");
    fs.writeFileSync(svgPath, SVG_ICON);

    // Генерируем иконки разных размеров
    const sizes = [192, 512];

    for (const size of sizes) {
      await sharp(svgPath)
        .resize(size, size, {
          fit: "contain",
          background: { r: 15, g: 23, b: 41 },
        })
        .png()
        .toFile(path.join(outputDir, `icon-${size}.png`));

      console.log(`✅ Создана icon-${size}.png`);

      // Генерируем maskable версию (для адаптивных иконок)
      await sharp(svgPath)
        .resize(size, size, {
          fit: "contain",
          background: { r: 15, g: 23, b: 41 },
        })
        .png()
        .toFile(path.join(outputDir, `icon-${size}-maskable.png`));

      console.log(`✅ Создана icon-${size}-maskable.png`);
    }

    // Создаём скриншот приложения
    const screenshotSvg = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 720">
      <rect width="540" height="720" fill="#0f1729"/>
      <text x="270" y="100" font-size="60" font-weight="bold" fill="#9333ea" text-anchor="middle">
        Погода
      </text>
      <rect x="50" y="150" width="440" height="60" rx="10" fill="#1f2937" stroke="#9333ea" stroke-width="2"/>
      <text x="270" y="185" font-size="20" fill="#9ca3af" text-anchor="middle">
        Введите город...
      </text>
      
      <rect x="50" y="250" width="440" height="60" rx="10" fill="#9333ea"/>
      <text x="270" y="290" font-size="20" fill="white" text-anchor="middle" font-weight="bold">
        Узнать погоду
      </text>
      
      <circle cx="135" cy="450" r="50" fill="#38bdf8" opacity="0.2"/>
      <text x="135" y="435" font-size="45" text-anchor="middle">☀️</text>
      <text x="135" y="530" font-size="16" fill="#9ca3af" text-anchor="middle">+25°C</text>
      
      <circle cx="405" cy="450" r="50" fill="#38bdf8" opacity="0.2"/>
      <text x="405" y="435" font-size="45" text-anchor="middle">💧</text>
      <text x="405" y="530" font-size="16" fill="#9ca3af" text-anchor="middle">65%</text>
    </svg>
    `;

    const screenshotPath = path.join(outputDir, "temp-screenshot.svg");
    fs.writeFileSync(screenshotPath, screenshotSvg);

    await sharp(screenshotPath)
      .resize(540, 720, { fit: "fill" })
      .png()
      .toFile(path.join(outputDir, "screenshot-540x720.png"));

    console.log(`✅ Создана screenshot-540x720.png`);

    // Удаляем временные файлы
    fs.unlinkSync(svgPath);
    fs.unlinkSync(screenshotPath);

    console.log("\n✨ Все иконки успешно созданы!");
    console.log(
      "📝 Обновите manifest.json, если нужны дополнительные размеры.",
    );
  } catch (error) {
    console.error("❌ Ошибка при генерации иконок:", error.message);
    process.exit(1);
  }
}

generateIcons();
