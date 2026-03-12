#!/usr/bin/env python3
"""
Скрипт для генерации PWA иконок
Требует: Python 3 + Pillow (PIL)
Установка: pip install Pillow
"""

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("❌ Пакет Pillow не установлен!")
    print("Установите: pip install Pillow")
    exit(1)

def create_icon(size, filename):
    """Создаёт иконку погодного приложения"""
    # Фон - темный цвет из темы #0f1729
    img = Image.new('RGB', (size, size), color=(15, 23, 41))
    draw = ImageDraw.Draw(img)
    
    # Солнце (жёлтое)
    sun_x, sun_y = size // 4, size // 4
    sun_radius = size // 8
    draw.ellipse(
        [sun_x - sun_radius, sun_y - sun_radius, 
         sun_x + sun_radius, sun_y + sun_radius],
        fill=(255, 215, 0)
    )
    
    # Облако (светло-голубое)
    cloud_y = size // 2
    cloud_x = size // 2
    cloud_width = size // 3
    cloud_height = size // 6
    
    # Используем эллипсы для облака
    draw.ellipse(
        [cloud_x - cloud_width, cloud_y - cloud_height // 2,
         cloud_x - cloud_width // 2, cloud_y + cloud_height // 2],
        fill=(232, 244, 248)
    )
    draw.ellipse(
        [cloud_x - cloud_width // 2, cloud_y - cloud_height,
         cloud_x + cloud_width // 2, cloud_y + cloud_height],
        fill=(232, 244, 248)
    )
    draw.ellipse(
        [cloud_x + cloud_width // 2, cloud_y - cloud_height // 2,
         cloud_x + cloud_width, cloud_y + cloud_height // 2],
        fill=(232, 244, 248)
    )
    
    # Капельки воды (синие)
    drop_radius = size // 20
    for i, x_pos in enumerate([cloud_x - cloud_width // 3, cloud_x, cloud_x + cloud_width // 3]):
        y_pos = cloud_y + cloud_height + drop_radius
        draw.ellipse(
            [x_pos - drop_radius, y_pos - drop_radius,
             x_pos + drop_radius, y_pos + drop_radius],
            fill=(77, 166, 255)
        )
    
    img.save(filename, 'PNG')
    return True

def create_screenshot():
    """Создаёт скриншот приложения"""
    img = Image.new('RGB', (540, 720), color=(15, 23, 41))
    draw = ImageDraw.Draw(img)
    
    # Простой дизайн - основные элементы UI
    # Заголовок
    draw.rectangle([0, 0, 540, 120], fill=(15, 23, 41))
    
    # Поле ввода
    draw.rectangle([25, 140, 515, 200], outline=(147, 51, 234, 200), width=2)
    
    # Кнопка
    draw.rectangle([25, 220, 515, 280], fill=(147, 51, 234))
    
    # Карточки погоды
    card_y = 320
    for i in range(3):
        draw.rectangle([25, card_y + i * 100, 515, card_y + i * 100 + 80], 
                       outline=(100, 100, 120), width=1, fill=(31, 41, 55))
    
    img.save('screenshot-540x720.png', 'PNG')
    return True

if __name__ == '__main__':
    print('📦 Генерирую PWA иконки...\n')
    
    try:
        create_icon(192, 'icon-192.png')
        print('✅ Создана icon-192.png')
        
        create_icon(192, 'icon-192-maskable.png')
        print('✅ Создана icon-192-maskable.png')
        
        create_icon(512, 'icon-512.png')
        print('✅ Создана icon-512.png')
        
        create_icon(512, 'icon-512-maskable.png')
        print('✅ Создана icon-512-maskable.png')
        
        create_screenshot()
        print('✅ Создана screenshot-540x720.png')
        
        print('\n✨ Все иконки успешно созданы!')
        print('\n💡 Рекомендация:')
        print('   Для улучшения внешнего вида иконок используйте:')
        print('   - Favicon Generator: https://www.favicon-generator.org/')
        print('   - PWA Builder: https://www.pwabuilder.com/')
        
    except Exception as e:
        print(f'❌ Ошибка: {e}')
        exit(1)
