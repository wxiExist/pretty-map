import json
from pathlib import Path

class MapStyle:
    """
    Base map style class with complete customization options.
    
    All attributes can be overridden in custom JSON files or subclasses.
    
    Color attributes accept hex color codes (#RRGGBB or #RGB)
    Alpha attributes are floats from 0.0 (fully transparent) to 1.0 (fully opaque)
    Font sizes are integers in points
    Widths are floats in pixels
    
    Customization Examples:
    - Change all colors for your theme
    - Adjust font sizes and thicknesses
    - Toggle water and building layers
    - Create high-contrast or pastel variations
    """

    def __init__(self):
        # Background
        self.bg_color = '#ffffff'
        
        # Streets
        self.street_color = '#000000'
        self.street_width = 0.5
        
        # Text - Title
        self.title_color = '#000000'
        self.title_size = 56
        
        # Text - Subtitle
        self.subtitle_color = '#666666'
        self.subtitle_size = 24
        
        # Water features
        self.draw_water = False
        self.water_color = '#a0c8ff'
        self.water_alpha = 0.35
        
        # Buildings
        self.draw_buildings = False
        self.building_color = '#c7c7c7'
        self.building_alpha = 0.5
        
        # Title box (optional background behind text)
        self.title_box = False
        self.title_box_color = '#000000'
        self.title_box_alpha = 0.22
        self.title_box_height = 0.12
    
    def get_config(self):
        return {
            'bg_color': self.bg_color,
            'street_color': self.street_color,
            'street_width': self.street_width,
            'title_color': self.title_color,
            'subtitle_color': self.subtitle_color,
            'title_size': self.title_size,
            'subtitle_size': self.subtitle_size,
            'draw_water': self.draw_water,
            'draw_buildings': self.draw_buildings,
            'water_color': self.water_color,
            'water_alpha': self.water_alpha,
            'building_color': self.building_color,
            'building_alpha': self.building_alpha,
            'title_box': self.title_box,
            'title_box_color': self.title_box_color,
            'title_box_alpha': self.title_box_alpha,
            'title_box_height': self.title_box_height
        }


class MinimalStyle(MapStyle):
    
    def __init__(self):
        super().__init__()
        self.bg_color = '#ffffff'
        self.street_color = '#000000'
        self.street_width = 0.8
        self.title_color = '#000000'
        self.subtitle_color = '#666666'


class BlueprintStyle(MapStyle):
    def __init__(self):
        super().__init__()
        self.bg_color = '#0a3d62'
        self.street_color = '#ffffff'
        self.street_width = 0.6
        self.title_color = '#ffffff'
        self.subtitle_color = '#a5b1c2'
        self.draw_buildings = True
        self.building_color = '#0f4c81'
        self.building_alpha = 0.35
        self.draw_water = True
        self.water_color = '#0c5b8f'
        self.water_alpha = 0.45
        self.title_box_color = '#041d2f'
        self.title_box_alpha = 0.35


class WatercolorStyle(MapStyle):
    def __init__(self):
        super().__init__()
        self.bg_color = '#f8f9fa'
        self.street_color = '#778ca3'
        self.street_width = 1.2
        self.title_color = '#4b6584'
        self.subtitle_color = '#95afc0'
        self.draw_buildings = True
        self.building_color = '#dfe6e9'
        self.building_alpha = 0.7
        self.draw_water = True
        self.water_color = '#c8dff8'
        self.water_alpha = 0.55
        self.title_box_color = '#ffffff'
        self.title_box_alpha = 0.6


class DarkStyle(MapStyle):
    
    def __init__(self):
        super().__init__()
        self.bg_color = '#1e1e1e'
        self.street_color = '#ffffff'
        self.street_width = 0.7
        self.title_color = '#ffffff'
        self.subtitle_color = '#a0a0a0'
        self.draw_water = True
        self.water_color = '#0f2b46'
        self.water_alpha = 0.7
        self.draw_buildings = True
        self.building_color = '#2b2b2b'
        self.building_alpha = 0.6
        self.title_box_color = '#0f0f0f'
        self.title_box_alpha = 0.35


class VintageStyle(MapStyle):
    
    def __init__(self):
        super().__init__()
        self.bg_color = '#f5e6d3'
        self.street_color = '#8b4513'
        self.street_width = 0.9
        self.title_color = '#5d4037'
        self.subtitle_color = '#8d6e63'
        self.draw_buildings = True
        self.building_color = '#e8d6bc'
        self.building_alpha = 0.7
        self.draw_water = True
        self.water_color = '#c0b090'
        self.water_alpha = 0.4
        self.title_box_color = '#d4c2a4'
        self.title_box_alpha = 0.5


class NeonStyle(MapStyle):
    
    def __init__(self):
        super().__init__()
        self.bg_color = '#0f0f23'
        self.street_color = '#00ffff'
        self.street_width = 1.0
        self.title_color = '#ff00ff'
        self.subtitle_color = '#00ffff'
        self.draw_water = True
        self.water_color = '#07163a'
        self.water_alpha = 0.75
        self.draw_buildings = True
        self.building_color = '#1a1a3a'
        self.building_alpha = 0.65
        self.title_box_color = '#050910'
        self.title_box_alpha = 0.55


class PastelStyle(MapStyle):
    
    def __init__(self):
        super().__init__()
        self.bg_color = '#fbf7f4'
        self.street_color = '#5f6b7a'
        self.street_width = 0.9
        self.title_color = '#414b57'
        self.subtitle_color = '#7b8794'
        self.draw_water = True
        self.water_color = '#d6e8ff'
        self.water_alpha = 0.65
        self.draw_buildings = True
        self.building_color = '#f2e9e4'
        self.building_alpha = 0.85
        self.title_box_color = '#ffffff'
        self.title_box_alpha = 0.65


class CopperStyle(MapStyle):
    
    def __init__(self):
        super().__init__()
        self.bg_color = '#1b1a17'
        self.street_color = '#f2c57c'
        self.street_width = 0.85
        self.title_color = '#f2c57c'
        self.subtitle_color = '#d9a441'
        self.draw_buildings = True
        self.building_color = '#3a2f23'
        self.building_alpha = 0.75
        self.draw_water = True
        self.water_color = '#1f2a33'
        self.water_alpha = 0.6
        self.title_box_color = '#0f0d0b'
        self.title_box_alpha = 0.45


class SandStyle(MapStyle):
    
    def __init__(self):
        super().__init__()
        self.bg_color = '#f3efe6'
        self.street_color = '#6f5f4d'
        self.street_width = 0.8
        self.title_color = '#5c4b3f'
        self.subtitle_color = '#8b7a6b'
        self.draw_buildings = True
        self.building_color = '#e3d6c5'
        self.building_alpha = 0.8
        self.draw_water = True
        self.water_color = "#aacbda"
        self.water_alpha = 0.55
        self.title_box_color = '#f7f1e8'
        self.title_box_alpha = 0.65


class NightSkyStyle(MapStyle):
    
    def __init__(self):
        super().__init__()
        self.bg_color = '#0b0f1a'
        self.street_color = '#7de2d1'
        self.street_width = 0.9
        self.title_color = '#e8f1ff'
        self.subtitle_color = '#b5c7e8'
        self.draw_water = True
        self.water_color = '#0f1f35'
        self.water_alpha = 0.75
        self.draw_buildings = True
        self.building_color = '#141a2a'
        self.building_alpha = 0.6
        self.title_box_color = '#060910'
        self.title_box_alpha = 0.55


class RedWaterStyle(MapStyle):
    
    def __init__(self):
        super().__init__()
        self.bg_color = '#f8f9fa'
        self.street_color = '#000000'
        self.street_width = 1.2
        self.title_color = '#000000'
        self.subtitle_color = '#333333'
        self.draw_buildings = True
        self.building_color = '#dfe6e9'
        self.building_alpha = 0.7
        self.draw_water = True
        self.water_color = '#d32f2f'
        self.water_alpha = 0.65
        self.title_box_color = '#ffffff'
        self.title_box_alpha = 0.6

AVAILABLE_STYLES = {
    'minimal': MinimalStyle,
    'blueprint': BlueprintStyle,
    'watercolor': WatercolorStyle,
    'dark': DarkStyle,
    'vintage': VintageStyle,
    'neon': NeonStyle,
    'pastel': PastelStyle,
    'copper': CopperStyle,
    'sand': SandStyle,
    'nightsky': NightSkyStyle,
    'waterred': RedWaterStyle
}


def get_style(style_name):
    style_class = AVAILABLE_STYLES.get(style_name.lower(), MinimalStyle)
    return style_class()


def list_styles():
    return list(AVAILABLE_STYLES.keys())


def load_custom_style(path, base_style='minimal'):
    base = get_style(base_style)
    config = base.get_config()
    style_path = Path(path)
    if not style_path.exists():
        raise FileNotFoundError(f"Файл стиля не найден: {style_path}")
    data = json.loads(style_path.read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError("JSON должен содержать объект с параметрами стиля")
    for key, value in data.items():
        if key in config:
            config[key] = value
    return config
