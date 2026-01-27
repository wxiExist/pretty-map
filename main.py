
import argparse
import sys
from pathlib import Path
from styles import get_style, list_styles, load_custom_style
from map_poster import create_map_poster


def main():
    parser = argparse.ArgumentParser(
        description='[+] Генератор красивых постеров карт городов',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s --city "Moscow" --style minimal
  %(prog)s --city "Paris, France" --style blueprint
  %(prog)s --coords 55.7558 37.6173 --style watercolor
  %(prog)s --city "London" --style dark --output london_map.png --size 4000 3000
  
Доступные стили: minimal, blueprint, watercolor, dark, vintage, neon
        """
    )

    location_group = parser.add_mutually_exclusive_group(required=False)
    location_group.add_argument(
        '--city',
        type=str,
        help='Название города (например, "Moscow", "New York, USA")'
    )
    location_group.add_argument(
        '--coords',
        nargs=2,
        type=float,
        metavar=('LAT', 'LON'),
        help='Координаты: широта и долгота (например, 55.7558 37.6173)'
    )

    parser.add_argument(
        '--style',
        type=str,
        default='minimal',
        choices=list_styles(),
        help='Стиль оформления (по умолчанию: minimal)'
    )
    parser.add_argument(
        '--custom-style',
        type=str,
        help='Путь к JSON с параметрами стиля (перекрывает выбранный стиль)'
    )
    parser.add_argument(
        '--title',
        type=str,
        help='Текст заголовка на постере (по умолчанию: название места)'
    )
    parser.add_argument(
        '--subtitle',
        type=str,
        help='Текст под заголовком (опционально)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='output/map_poster.png',
        help='Путь к выходному файлу (по умолчанию: output/map_poster.png)'
    )
    parser.add_argument(
        '--size',
        nargs=2,
        type=int,
        metavar=('WIDTH', 'HEIGHT'),
        default=[3000, 4000],
        help='Размер изображения в пикселях: ширина высота (по умолчанию: 3000 4000)'
    )
    parser.add_argument(
        '--radius',
        type=int,
        default=5000,
        help='Радиус области карты в метрах (по умолчанию: 5000)'
    )
    parser.add_argument(
        '--list-styles',
        action='store_true',
        help='Показать все доступные стили'
    )
    parser.add_argument(
        '--export-layers',
        type=str,
        help='Экспортировать слои в отдельные PNG файлы (например, --export-layers ./layers/). Создаёт файлы для редактирования в Фотошопе'
    )
    
    args = parser.parse_args()
    
    if args.list_styles:
        print("\n[+] Доступные стили:\n")
        for style_name in list_styles():
            style_obj = get_style(style_name)
            print(f"  • {style_name:12} - фон: {style_obj.bg_color}, улицы: {style_obj.street_color}")
        print()
        return 0

    if not args.city and not args.coords:
        parser.error("Необходимо указать --city или --coords")

    print("\n" + "="*60)
    print("[+]  MAP POSTER GENERATOR")
    print("="*60 + "\n")
    
    style = get_style(args.style)
    style_config = style.get_config()
    if args.custom_style:
        style_config = load_custom_style(args.custom_style, base_style=args.style)
    
    print(f"📍 Локация: ", end='')
    if args.city:
        print(f"{args.city}")
        location = args.city
        lat, lon = None, None
    else:
        print(f"Координаты {args.coords[0]}, {args.coords[1]}")
        location = None
        lat, lon = args.coords[0], args.coords[1]
    
    print(f"[+] Стиль: {args.style}" + (" + custom" if args.custom_style else ""))
    print(f"[+] Размер: {args.size[0]}x{args.size[1]} пикселей")
    print(f"[+] Радиус: {args.radius} метров")
    if args.title:
        print(f"[+] Заголовок: {args.title}")
    if args.subtitle:
        print(f"[+]  Подзаголовок: {args.subtitle}")
    print(f"[+] Выходной файл: {args.output}")
    if args.export_layers:
        print(f"[+] Экспорт слоёв: {args.export_layers}")
    print()
    
    try:
        output_path = create_map_poster(
            location=location,
            lat=lat,
            lon=lon,
            style_config=style_config,
            radius=args.radius,
            output_path=args.output,
            width=args.size[0],
            height=args.size[1],
            title_text=args.title,
            subtitle_text=args.subtitle,
            export_layers=args.export_layers
        )
        
        print(f"\n[+] Успех! Постер создан: {Path(output_path).absolute()}")
        print("="*60 + "\n")
        return 0
        
    except KeyboardInterrupt:
        print("\n\n[-]  Прервано пользователем")
        return 1
    except Exception as e:
        print(f"\n[-] Ошибка: {e}")
        import traceback
        print("\nПодробности:")
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
