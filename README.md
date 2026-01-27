# Pretty Map
A Python-based tool for generating beautiful, customizable map posters from OpenStreetMap data. Create stunning wall art featuring city maps with multiple visual styles, including building footprints, water features, and road networks.

### Examples
<img width="300" height="400" alt="Moscow" src="https://github.com/user-attachments/assets/48491107-1862-43c2-88f2-fe4696804c5c" />
<img width="300" height="400" alt="London" src="https://github.com/user-attachments/assets/6b67c800-a31a-4af8-97ea-dd3bbaaae11e" />
<img width="300" height="400" alt="MAI1" src="https://github.com/user-attachments/assets/89e33cdc-1e87-4a84-9708-9b87751c1b8f" />
<img width="300" height="400" alt="Paris" src="https://github.com/user-attachments/assets/092d3de5-e5d4-40b1-ad3d-da42f2d98e0c" />
<img width="300" height="400" alt="paris_borderless-test" src="https://github.com/user-attachments/assets/6a68ffa0-8337-42d0-9224-d05fe5dd84d5" />
<img width="300" height="400" alt="paris_NEO" src="https://github.com/user-attachments/assets/4053367f-517e-43ef-bc50-28213efea80b" />







## Features

- Generate map posters from city names or GPS coordinates
- 11 built-in visual styles (minimal, blueprint, watercolor, neon, vintage, and more)
- Custom style support via JSON configuration with full parameter customization
- Multi-layer rendering: water bodies, buildings, streets
- **Borderless mode**: map fades to background at edges with text placed at bottom
- Export in PNG or SVG format (scalable vector graphics)
- Export individual layers as separate PNG files for Photoshop editing
- Configurable text, colors, typography, and all visual parameters
- Progress indication with percentage bars during data download and rendering
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
- `--format FORMAT` - Output format: png or svg (default: png)
- `--borderless` - Borderless mode: map fades to background at edges, text placed at bottom
- `--export-layers PATH` - Export individual layers as PNG files to the specified directory for Photoshop editing (e.g., --export-layers ./layers/)

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

**Exporting layers for Photoshop editing:**
```bash
python main.py --city "Barcelona" --style watercolor --export-layers ./barcelona_layers/
```
This creates separate PNG files for water, buildings, and streets with transparency, allowing further editing in Photoshop.

**SVG vector export (scalable and editable):**
```bash
python main.py --city "Rome" --style minimal --format svg --output rome.svg
```

**SVG with custom style:**
```bash
python main.py --coords 40.7128 -74.0060 --style blueprint --format svg --output nyc.svg
```

**Borderless mode (fade to background, text at bottom):**
```bash
python main.py --city "Tokyo" --style minimal --borderless --output tokyo_borderless.png
```

**Borderless with custom style:**
```bash
python main.py --city "Paris" --style watercolor --borderless --title "PARIS" --subtitle "City of Light" --output paris_borderless.png
```



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

Create your own visual style using a JSON configuration file. All parameters are optional and can be freely customized.

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

### Parameter Reference - Complete Customization

**Background and Streets:**
- `bg_color` - Background color (hex code, e.g., #ffffff, #1e1e1e)
- `street_color` - Street line color (hex code)
- `street_width` - Street line thickness in pixels (float, typical: 0.3-1.5)

**Typography - Full Control:**
- `title_color` - Main title text color (hex code)
- `title_size` - Title font size in points (int, typical: 50-80)
- `subtitle_color` - Subtitle text color (hex code)
- `subtitle_size` - Subtitle font size in points (int, typical: 20-30)

**Water Features - Customizable:**
- `draw_water` - Enable water layer rendering (boolean: true/false)
- `water_color` - Water body fill color (hex code)
- `water_alpha` - Water transparency level (float from 0.0 to 1.0, where 0.0 is transparent, 1.0 is opaque)

**Building Footprints - Customizable:**
- `draw_buildings` - Enable building footprints layer (boolean: true/false)
- `building_color` - Building fill color (hex code)
- `building_alpha` - Building transparency level (float from 0.0 to 1.0)

**Title Box (Optional):**
- `title_box` - Add colored background behind title text (boolean)
- `title_box_color` - Title box background color (hex code)
- `title_box_alpha` - Title box transparency (float from 0.0 to 1.0)
- `title_box_height` - Title box height as fraction of image height (float, typical: 0.08-0.15)

### Using Custom Styles

You can base your custom style on an existing built-in style:

```bash
python main.py --city "Berlin" --custom-style mystyle.json --output berlin.png
```

### Custom Style Examples

**Example 1: Vibrant Purple with Gold Streets**
```json
{
  "bg_color": "#2d1b4e",
  "street_color": "#ffd700",
  "street_width": 0.8,
  "title_color": "#ffd700",
  "subtitle_color": "#c0a0f0",
  "draw_water": true,
  "water_color": "#4a3a7a",
  "water_alpha": 0.6,
  "draw_buildings": true,
  "building_color": "#5d3f7a",
  "building_alpha": 0.6
}
```

**Example 2: Forest Green with Nature Theme**
```json
{
  "bg_color": "#f5f9f5",
  "street_color": "#2d5016",
  "street_width": 0.9,
  "title_color": "#1b3a0a",
  "subtitle_color": "#4a7c2f",
  "draw_water": true,
  "water_color": "#6db3e8",
  "water_alpha": 0.7,
  "draw_buildings": true,
  "building_color": "#d4e8c1",
  "building_alpha": 0.8
}
```

**Example 3: High Contrast Black & Yellow (Accessibility)**
```json
{
  "bg_color": "#ffffff",
  "street_color": "#000000",
  "street_width": 1.2,
  "title_color": "#ffcc00",
  "subtitle_color": "#000000",
  "title_size": 72,
  "subtitle_size": 28,
  "draw_water": true,
  "water_color": "#0066ff",
  "water_alpha": 0.8,
  "draw_buildings": true,
  "building_color": "#cccccc",
  "building_alpha": 0.9
}
```

See `example_custom_style.json` for a complete template.


## Technical Details

### Data Source

All map data is retrieved from OpenStreetMap via the Overpass API using the OSMnx library. The tool automatically handles:

- Geocoding of place names to coordinates
- Street network extraction
- Building footprint queries
- Water body geometry retrieval

### Progress Indication

The tool displays progress bars during:
- **Data Download**: Shows steps for coordinate geocoding and network data retrieval
- **Poster Creation**: Shows steps for layer loading, rendering water, buildings, streets, and final save

This helps you track long operations on large map areas.

### Layer Export

When using `--export-layers`, the tool creates separate PNG files for each rendered layer:

- **water.png** - Water bodies with alpha transparency
- **buildings.png** - Building footprints with alpha transparency  
- **streets.png** - Street network with alpha transparency
- **map_poster.png** - Final composite (in same output directory)

All layer files use transparent backgrounds, making them perfect for:
- Importing into Photoshop or Illustrator for further editing
- Selective layer visibility toggling
- Color adjustment per layer
- Custom composition and effects

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

**PNG Format (default):**
Generated images are saved as PNG files with:
- Default resolution: 3000x4000 pixels
- High DPI (300) suitable for printing
- Customizable dimensions via `--size` argument
- 7% top margin for title text
- 93% main map area
- Optional separate layer exports with transparency

**SVG Format (vector):**
When using `--format svg`, posters are exported as scalable vector graphics:
- Infinitely scalable without quality loss
- Editable text and paths in vector editors (Illustrator, Inkscape, etc.)
- Smaller file size for simple maps
- Perfect for professional printing and design work
- No DPI setting required (resolution-independent)

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
- Try `--borderless` for modern, edge-to-edge aesthetic with bottom-placed text

**Borderless Mode:**
- Perfect for modern, frameless prints
- Map smoothly fades to background color at edges (15% fade zone)
- Text automatically positioned at bottom for better composition
- Combines well with minimal or dark styles for contemporary look

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
