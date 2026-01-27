
import argparse
import sys
from pathlib import Path
from styles import get_style, list_styles, load_custom_style
from map_poster import create_map_poster


def main():
    parser = argparse.ArgumentParser(
        description='[+] Beautiful city map poster generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  %(prog)s --city "Moscow" --style minimal
  %(prog)s --city "Paris, France" --style blueprint
  %(prog)s --coords 55.7558 37.6173 --style watercolor
  %(prog)s --city "London" --style dark --output london_map.png --size 4000 3000
  %(prog)s --city "Tokyo" --format svg --output tokyo.svg
  
Available styles: minimal, blueprint, watercolor, dark, vintage, neon
        """
    )

    location_group = parser.add_mutually_exclusive_group(required=False)
    location_group.add_argument(
        '--city',
        type=str,
        help='City name (e.g., "Moscow", "New York, USA")'
    )
    location_group.add_argument(
        '--coords',
        nargs=2,
        type=float,
        metavar=('LAT', 'LON'),
        help='Coordinates: latitude and longitude (e.g., 55.7558 37.6173)'
    )

    parser.add_argument(
        '--style',
        type=str,
        default='minimal',
        choices=list_styles(),
        help='Visual style (default: minimal)'
    )
    parser.add_argument(
        '--custom-style',
        type=str,
        help='Path to custom style JSON file (overrides selected style)'
    )
    parser.add_argument(
        '--title',
        type=str,
        help='Poster title text (default: location name)'
    )
    parser.add_argument(
        '--subtitle',
        type=str,
        help='Subtitle text below title (optional)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='output/map_poster.png',
        help='Output file path (default: output/map_poster.png)'
    )
    parser.add_argument(
        '--size',
        nargs=2,
        type=int,
        metavar=('WIDTH', 'HEIGHT'),
        default=[3000, 4000],
        help='Image size in pixels: width height (default: 3000 4000)'
    )
    parser.add_argument(
        '--radius',
        type=int,
        default=5000,
        help='Map area radius in meters (default: 5000)'
    )
    parser.add_argument(
        '--format',
        type=str,
        default='png',
        choices=['png', 'svg'],
        help='Output format: png or svg (default: png)'
    )
    parser.add_argument(
        '--list-styles',
        action='store_true',
        help='Show all available styles'
    )
    parser.add_argument(
        '--export-layers',
        type=str,
        help='Export layers as separate PNG files (e.g., --export-layers ./layers/). Creates files for Photoshop editing'
    )
    
    args = parser.parse_args()
    
    if args.list_styles:
        print("\n[+] Available styles:\n")
        for style_name in list_styles():
            style_obj = get_style(style_name)
            print(f"  • {style_name:12} - bg: {style_obj.bg_color}, streets: {style_obj.street_color}")
        print()
        return 0

    if not args.city and not args.coords:
        parser.error("Must specify --city or --coords")

    print("\n" + "="*60)
    print("[+]  MAP POSTER GENERATOR")
    print("="*60 + "\n")
    
    style = get_style(args.style)
    style_config = style.get_config()
    if args.custom_style:
        style_config = load_custom_style(args.custom_style, base_style=args.style)
    
    print(f"📍 Location: ", end='')
    if args.city:
        print(f"{args.city}")
        location = args.city
        lat, lon = None, None
    else:
        print(f"Coordinates {args.coords[0]}, {args.coords[1]}")
        location = None
        lat, lon = args.coords[0], args.coords[1]
    
    print(f"[+] Style: {args.style}" + (" + custom" if args.custom_style else ""))
    print(f"[+] Size: {args.size[0]}x{args.size[1]} pixels")
    print(f"[+] Radius: {args.radius} meters")
    print(f"[+] Format: {args.format}")
    if args.title:
        print(f"[+] Title: {args.title}")
    if args.subtitle:
        print(f"[+] Subtitle: {args.subtitle}")
    print(f"[+] Output file: {args.output}")
    if args.export_layers:
        print(f"[+] Export layers: {args.export_layers}")
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
            export_layers=args.export_layers,
            output_format=args.format
        )
        
        print(f"\n[+] Success! Poster created: {Path(output_path).absolute()}")
        print("="*60 + "\n")
        return 0
        
    except KeyboardInterrupt:
        print("\n\n[-] Interrupted by user")
        return 1
    except Exception as e:
        print(f"\n[-] Error: {e}")
        import traceback
        print("\nDetails:")
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
