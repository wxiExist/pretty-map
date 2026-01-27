import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import numpy as np
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')
ox.config(log_console=False, use_cache=True)


def print_progress(current, total, label=""):
    """Выводит прогресс в процентах"""
    if total <= 0:
        return
    progress = (current / total) * 100
    bar_length = 30
    filled = int((progress / 100) * bar_length)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f"[{bar}] {progress:.1f}% - {label}", end='\r')


class MapPosterGenerator:
    
    def __init__(self, style_config):
        self.style = style_config
        
    def fetch_map_data(self, location=None, lat=None, lon=None, radius=5000):
        print(f"Загрузка данных карты...")
        print_progress(0, 3, "Подготовка координат")
        if radius > 6000:
            custom_filter = '["highway"~"motorway|trunk|primary|secondary"]'
        else:
            custom_filter = None
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if location:
                    print_progress(1, 3, "Геокодирование")
                    center_lat, center_lon = ox.geocode(location)
                elif lat is not None and lon is not None:
                    center_lat, center_lon = lat, lon
                else:
                    raise ValueError("Необходимо указать либо location, либо координаты (lat, lon)")
                
                print_progress(2, 3, "Загрузка данных графа")
                graph = ox.graph_from_point(
                    (center_lat, center_lon),
                    dist=radius,
                    network_type='all',
                    simplify=True,
                    custom_filter=custom_filter
                )
                
                print_progress(3, 3, "Завершено")
                print()
                
                if location:
                    place_name = location
                else:
                    place_name = f"{lat:.4f}°, {lon:.4f}°"
                
                print(f"✓ Данные загружены: {len(graph.nodes)} узлов, {len(graph.edges)} рёбер")
                return graph, place_name, (center_lat, center_lon)
                
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"\n⚠️  Ошибка при загрузке (попытка {attempt + 1}/{max_retries}), повтор через 5 сек...")
                    import time
                    time.sleep(5)
                else:
                    print(f"\nОшибка при загрузке данных: {e}")
                    raise
    
    def fetch_layers(self, center_lat, center_lon, radius):
        if center_lat is None or center_lon is None:
            return None, None
        tags = {}
        if self.style.get('draw_buildings'):
            tags['building'] = True
        if self.style.get('draw_water'):
            tags['water'] = True
            tags['waterway'] = True
            tags['natural'] = ['water', 'bay', 'harbour', 'coastline']
        if not tags:
            return None, None
        try:
            gdf = ox.geometries_from_point((center_lat, center_lon), dist=radius, tags=tags)
        except Exception as e:
            print(f"⚠️  Не удалось загрузить слои зданий/воды: {e}")
            return None, None
        buildings = None
        water = None
        if 'building' in gdf.columns:
            buildings = gdf[gdf['building'].notna()].copy()
        water_cols = [c for c in ('water', 'waterway', 'natural') if c in gdf.columns]
        if water_cols:
            water = gdf[gdf[water_cols].notna().any(axis=1)].copy()
        return buildings, water
    
    def create_poster(self, graph, place_name, output_path, figsize=(12, 16),
                      center_lat=None, center_lon=None, radius=5000,
                      title_text=None, subtitle_text=None, export_layers=None):
        print(f"Создание постера...")
        title_text = (title_text or place_name).upper()
        subtitle_text = subtitle_text or None

        fig = plt.figure(figsize=figsize, facecolor=self.style['bg_color'])
        ax = fig.add_axes([0, 0, 1, 0.93])
        ax.set_facecolor(self.style['bg_color'])
        
        print_progress(1, 5, "Загрузка слоёв")
        buildings, water = self.fetch_layers(center_lat, center_lon, radius)
        
        # Список слоёв для экспорта
        layers = {}
        
        print_progress(2, 5, "Рисование воды")
        if water is not None and not water.empty and self.style.get('draw_water'):
            water.plot(ax=ax,
                       facecolor=self.style.get('water_color', '#a0c8ff'),
                       edgecolor='none',
                       alpha=self.style.get('water_alpha', 0.35),
                       linewidth=0,
                       markersize=0,
                       zorder=1)
            if export_layers:
                layers['water'] = (water, self.style.get('water_color', '#a0c8ff'), 
                                 self.style.get('water_alpha', 0.35), figsize)
        
        print_progress(3, 5, "Рисование зданий")
        if buildings is not None and not buildings.empty and self.style.get('draw_buildings'):
            buildings.plot(ax=ax,
                           facecolor=self.style.get('building_color', '#c7c7c7'),
                           edgecolor='none',
                           alpha=self.style.get('building_alpha', 0.5),
                           linewidth=0,
                           markersize=0,
                           zorder=2)
            if export_layers:
                layers['buildings'] = (buildings, self.style.get('building_color', '#c7c7c7'), 
                                     self.style.get('building_alpha', 0.5), figsize)
        
        print_progress(4, 5, "Рисование улиц")
        ox.plot_graph(
            graph,
            ax=ax,
            node_size=0,
            edge_color=self.style['street_color'],
            edge_linewidth=self.style['street_width'],
            bgcolor=self.style['bg_color'],
            show=False,
            close=False
        )
        if export_layers:
            layers['streets'] = (graph, self.style['street_color'], 
                               self.style['street_width'], figsize)
        
        ax.axis('off')
        ax.margins(0)
        fig.text(
            0.5, 0.96,
            title_text,
            ha='center',
            va='top',
            fontsize=self.style['title_size'],
            color=self.style['title_color'],
            fontweight='bold',
            fontfamily='sans-serif'
        )

        if subtitle_text:
            fig.text(
                0.5, 0.92,
                subtitle_text,
                ha='center',
                va='top',
                fontsize=self.style['subtitle_size'],
                color=self.style['subtitle_color'],
                fontfamily='sans-serif'
            )

        print_progress(5, 5, "Сохранение результатов")
        fig.savefig(
            output_path,
            dpi=300,
            facecolor=self.style['bg_color'],
            edgecolor='none'
        )
        plt.close(fig)
        
        print()
        print(f"[+] Постер сохранён: {output_path}")
        
        # Экспорт слоёв если требуется
        if export_layers and layers:
            self._export_layers(layers, export_layers, figsize, self.style)
    
    def _export_layers(self, layers, export_dir, figsize, style):
        """Экспортирует каждый слой в отдельный PNG файл"""
        export_path = Path(export_dir)
        export_path.mkdir(parents=True, exist_ok=True)
        
        print(f"\n[+] Экспорт слоёв в {export_dir}")
        
        layer_count = len(layers)
        for idx, (layer_name, layer_data) in enumerate(layers.items(), 1):
            print_progress(idx, layer_count, f"Экспорт слоя: {layer_name}")
            
            data, color, alpha, size = layer_data
            
            # Создаём новый прозрачный фон для слоя
            fig = plt.figure(figsize=size, facecolor='none')
            ax = fig.add_axes([0, 0, 1, 1])
            ax.set_facecolor('none')
            
            try:
                if layer_name == 'streets':
                    # Для графа улиц
                    ox.plot_graph(
                        data,
                        ax=ax,
                        node_size=0,
                        edge_color=color,
                        edge_linewidth=alpha,  # Используем alpha как ширину линии
                        bgcolor='none',
                        show=False,
                        close=False
                    )
                else:
                    # Для GeoDataFrame (зданий и воды)
                    data.plot(ax=ax,
                             facecolor=color,
                             edgecolor='none',
                             alpha=alpha,
                             linewidth=0,
                             markersize=0)
            except Exception as e:
                print(f"\n⚠️  Не удалось экспортировать слой {layer_name}: {e}")
                plt.close(fig)
                continue
            
            ax.axis('off')
            ax.margins(0)
            
            output_file = export_path / f"{layer_name}.png"
            fig.savefig(
                output_file,
                dpi=300,
                transparent=True,
                bbox_inches='tight',
                pad_inches=0
            )
            plt.close(fig)
        
        print()
        print(f"[+] Слои экспортированы в {export_path.absolute()}")
    
    def generate(self, location=None, lat=None, lon=None, radius=5000, 
                 output_path='map_poster.png', figsize=(12, 16),
                 title_text=None, subtitle_text=None, export_layers=None):

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        graph, place_name, (center_lat, center_lon) = self.fetch_map_data(location, lat, lon, radius)

        self.create_poster(
            graph,
            place_name,
            output_path,
            figsize,
            center_lat,
            center_lon,
            radius,
            title_text,
            subtitle_text,
            export_layers
        )
        
        return output_path


def create_map_poster(location=None, lat=None, lon=None, style_config=None,
                     radius=5000, output_path='map_poster.png', width=3000, height=4000,
                     title_text=None, subtitle_text=None, export_layers=None):

    figsize = (width / 300, height / 300)

    generator = MapPosterGenerator(style_config)

    return generator.generate(
        location=location,
        lat=lat,
        lon=lon,
        radius=radius,
        output_path=output_path,
        figsize=figsize,
        title_text=title_text,
        subtitle_text=subtitle_text,
        export_layers=export_layers
    )
