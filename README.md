# Pretty Map

A Python-based tool for generating beautiful, customizable map posters from OpenStreetMap data. Create stunning wall art featuring city maps with multiple visual styles, including building footprints, water features, and road networks.

## Features

- Generate map posters from city names or GPS coordinates
- 11 built-in visual styles (minimal, blueprint, watercolor, neon, vintage, and more)
- Custom style support via JSON configuration
- Multi-layer rendering: water bodies, buildings, streets
- Configurable text, colors, and typography
- Automatic map simplification for large areas
- High-resolution output suitable for printing

## Installation

### Requirements

- Python 3.10 or higher
- pip package manager

### Setup

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

**Dependencies:**
- osmnx 1.9.2 - OpenStreetMap data retrieval
- matplotlib 3.8.2 - Visualization
- geopandas 0.14.2 - Geographic data handling
- shapely 2.0.2 - Geometric operations
- Pillow 10.2.0 - Image processing

## Usage

### Basic Usage

Generate a poster using a city name:

```bash
python main.py --city "Paris" --style watercolor --output paris.png
```

Generate a poster using coordinates:

```bash
python main.py --coords 48.8566 2.3522 --style minimal --output paris.png
```

### Command-Line Arguments

#### Location (required, choose one)

- `--city CITY` - City or place name (e.g., "New York", "Tokyo")
- `--coords LAT LON` - GPS coordinates in decimal degrees

#### Style Options

- `--style STYLE` - Built-in style name (default: minimal)
- `--custom-style PATH` - Path to custom style JSON file
- `--list-styles` - Display all available built-in styles

#### Text Customization

- `--title TEXT` - Custom poster title (default: location name)
- `--subtitle TEXT` - Subtitle text below title (optional)

#### Output Configuration

- `--output PATH` - Output file path (default: map_poster.png)
- `--size WIDTH HEIGHT` - Image dimensions in pixels (default: 3000 4000)
- `--radius METERS` - Map area radius in meters (default: 5000)

### Examples

**Simple minimal poster:**
```bash
python main.py --city "London" --output london.png
```

**Large area with custom text:**
```bash
python main.py --city "Tokyo" --radius 8000 --title "TOKYO" --subtitle "35.6762° N, 139.6503° E" --output tokyo_large.png
```

**Watercolor style with buildings:**
```bash
python main.py --coords 51.5074 -0.1278 --style watercolor --output london_watercolor.png
```

**Custom poster dimensions:**
```bash
python main.py --city "Venice" --style nightsky --size 2400 3600 --output venice_vertical.png
```

**Using a custom style:**
```bash
python main.py --city "Amsterdam" --custom-style my_style.json --output amsterdam_custom.png
```

### Examples (Imgs)
<img width="300" height="400" alt="Moscow" src="https://github.com/user-attachments/assets/68b9e1f9-c032-46a5-bcaf-f64414352555" />
<img width="300" height="400" alt="London" src="https://github.com/user-attachments/assets/1c39cd87-4b19-49d8-9db8-37e67d4190ba" />
<img width="300" height="400" alt="MAI1" src="https://github.com/user-attachments/assets/a4b71276-1bf7-48d6-99de-62f2f76e93fc" />
<img width="311" height="241" alt="paris_pastel" src="https://github.com/user-attachments/assets/00371a65-d768-4218-a995-113d644d41d8" />


## Built-in Styles

The generator includes 11 pre-configured visual styles:

1. **minimal** - Clean black lines on white background
2. **blueprint** - Architect-style white on blue with buildings
3. **watercolor** - Soft blue tones with water features
4. **dark** - White streets on dark background
5. **vintage** - Sepia-toned classic map aesthetic
6. **neon** - Vibrant cyan on dark purple
7. **pastel** - Soft pink tones with building details
8. **copper** - Warm bronze and cream palette
9. **sand** - Desert-inspired beige and brown
10. **nightsky** - Deep navy with golden streets
11. **waterred** - Black and red with red water bodies

View all styles:
```bash
python main.py --list-styles
```

## Custom Styles

Create your own visual style using a JSON configuration file.

### Custom Style Format

All parameters are optional. Unspecified values inherit from the base style.

```json
{
  "bg_color": "#ffffff",
  "street_color": "#000000",
  "street_width": 0.5,
  
  "title_color": "#000000",
  "subtitle_color": "#666666",
  "title_size": 65,
  "subtitle_size": 26,
  
  "draw_water": true,
  "water_color": "#a0c8ff",
  "water_alpha": 0.6,
  
  "draw_buildings": true,
  "building_color": "#c7c7c7",
  "building_alpha": 0.75,
  
  "title_box": false,
  "title_box_color": "#ffffff",
  "title_box_alpha": 0.65,
  "title_box_height": 0.12
}
```

### Parameter Reference

**Colors and Streets:**
- `bg_color` - Background color (hex code)
- `street_color` - Street line color (hex code)
- `street_width` - Street line thickness (float, typical: 0.3-1.5)

**Typography:**
- `title_color` - Main title text color (hex code)
- `subtitle_color` - Subtitle text color (hex code)
- `title_size` - Title font size (int, typical: 50-80)
- `subtitle_size` - Subtitle font size (int, typical: 20-30)

**Water Features:**
- `draw_water` - Enable water layer rendering (boolean)
- `water_color` - Water body fill color (hex code)
- `water_alpha` - Water transparency (float, 0.0-1.0)

**Buildings:**
- `draw_buildings` - Enable building footprints (boolean)
- `building_color` - Building fill color (hex code)
- `building_alpha` - Building transparency (float, 0.0-1.0)

**Title Box (deprecated, recommend keeping false):**
- `title_box` - Add background behind title text (boolean)
- `title_box_color` - Title box background color (hex code)
- `title_box_alpha` - Title box transparency (float, 0.0-1.0)
- `title_box_height` - Title box height as fraction of image (float, typical: 0.08-0.15)

### Using Custom Styles

You can base your custom style on an existing built-in style:

```bash
python main.py --city "Berlin" --custom-style mystyle.json --output berlin.png
```

Or specify a base style explicitly in your code by modifying the custom style loading logic.

See `example_custom_style.json` for a complete template.

## Technical Details

### Data Source

All map data is retrieved from OpenStreetMap via the Overpass API using the OSMnx library. The tool automatically handles:

- Geocoding of place names to coordinates
- Street network extraction
- Building footprint queries
- Water body geometry retrieval

### Map Simplification

For large areas (radius > 6000m), the generator automatically filters street networks to show only major roads (motorways, trunk roads, primary and secondary highways). This prevents visual clutter on wide-area posters.

### Layer Rendering

Posters are rendered in layers from bottom to top:

1. Background color
2. Water bodies (if enabled)
3. Building footprints (if enabled)
4. Street network
5. Title and subtitle text

### Output Format

Generated images are saved as PNG files with:
- Default resolution: 3000x4000 pixels
- Customizable dimensions via `--size` argument
- 7% top margin for title text
- 93% main map area

### Network Errors

The tool includes automatic retry logic (3 attempts with 5-second delays) to handle temporary Overpass API unavailability or network issues.

## Project Structure

```
map/
├── main.py                    # CLI entry point
├── map_poster.py              # Core map generation engine
├── styles.py                  # Style definitions and custom style loader
├── requirements.txt           # Python dependencies
├── example_custom_style.json  # Custom style template
└── output/                    # Generated posters (created automatically)
```

## Tips for Best Results

**Choosing Radius:**
- Small urban areas: 2000-4000m
- City centers: 5000-7000m
- Large metropolitan areas: 8000-12000m

**Style Selection:**
- Use `blueprint`, `watercolor`, or `pastel` for detailed building-rich areas
- Use `minimal` or `dark` for clean, modern aesthetic
- Use `nightsky` or `copper` for decorative wall art

**Text Customization:**
- Keep titles short (1-2 words) for best visual impact
- Use subtitles for coordinates, dates, or additional context
- Leave subtitle empty for minimalist designs

**Performance:**
- Large radius values (>10km) may take several minutes to process
- Dense urban areas require more processing time than rural areas
- Network speed affects data download time

## Troubleshooting

**Issue: "UnboundLocalError" or network timeout**
- Solution: The tool will automatically retry. Wait for completion or try again later if Overpass API is overloaded.

**Issue: "No buildings/water found"**
- Solution: This is normal for areas without building data or water bodies in OpenStreetMap. The poster will render streets only.

**Issue: Map appears too cluttered**
- Solution: Increase radius (automatic simplification activates at 6km) or use a minimal style.

**Issue: Image dimensions are wrong**
- Solution: Specify custom size with `--size WIDTH HEIGHT` (e.g., `--size 2400 3600`).

## License

This project uses OpenStreetMap data, which is available under the Open Database License (ODbL). Generated posters should credit OpenStreetMap contributors when shared publicly.

## Acknowledgments

Built with OSMnx library by Geoff Boeing. Map data from OpenStreetMap and contributors.
