import threading
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
from datetime import datetime
from noise.tracker import NoiseTracker


class VisualMap:
    """
    Visualize graphical tracts, population density and noise heatmap.
    
    Folium Map Tutorial: https://vverde.github.io/blob/interactivechoropleth.html
    """
    
    def __init__(self, noise_track: NoiseTracker):
        # Store the reference of NoiseTracker to track noise data
        self.noise_tracker = noise_track
        self.geo = gpd.read_file('recourses/shown_geography.geojson')
        self.pd_data = pd.read_csv('recourses/shown_tract_popdensity2010.csv')
        self.pop = self.geo.merge(self.pd_data, left_on="id2", right_on="tract")
        self.x_map = self.geo.centroid.x.mean()
        self.y_map = self.geo.centroid.y.mean()
        self.scale = list(self.pd_data["Population_Density_in_2010"].quantile([0, 0.2, 0.4, 0.6, 0.8, 1]))
        self.timer = threading.Timer(10, self.plot_heatmap)
        self.timer.start()
        
    def plot_heatmap(self):
        # Create a base map
        mymap = folium.Map(location=[self.y_map, self.x_map], zoom_start=13, tiles=None)
        # Set tile layer style
        folium.TileLayer('CartoDB positron', name="Light Map", control=False).add_to(mymap)
        # Create a choropleth and add it to the base map
        folium.Choropleth(
            geo_data=self.geo,
            name='Choropleth',
            data=self.pd_data,
            columns=['tract', 'Population_Density_in_2010'],
            key_on="properties.id2",
            fill_color='YlGnBu',
            threshold_scale=self.scale,
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Population Density',
            smooth_factor=0
        ).add_to(mymap)
        
        style_function = lambda x: {'fillColor': '#ffffff',
                                    'color': '#000000',
                                    'fillOpacity': 0.1,
                                    'weight': 0.1}
        
        highlight_function = lambda x: {'fillColor': '#000000',
                                        'color': '#000000',
                                        'fillOpacity': 0.50,
                                        'weight': 0.1}
        
        # Create a geo popup layer
        NIL = folium.features.GeoJson(
            self.pop,
            style_function=style_function,
            control=False,
            highlight_function=highlight_function,
            tooltip=folium.features.GeoJsonTooltip(
                fields=['tract', 'Name', 'Population_Density_in_2010'],
                aliases=['Tract: ', 'Name: ', 'Population Density (people in per sq mi): '],
                style="background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"
            )
        )
        mymap.add_child(NIL)
        mymap.keep_in_front(NIL)

        # Create a noise heatmap
        heatmap = HeatMap(self.noise_tracker.noise, radius=15)
        mymap.add_child(heatmap)
        mymap.keep_in_front(heatmap)
        folium.LayerControl().add_to(mymap)
        
        # Save the final map as html files
        now = datetime.now()
        name = now.strftime("%m-%d_%H-%M-%S")
        mymap.save('visual/HeatMaps/' + name + '.html')  # 保存为HTML
        print("New heatmap has been saved to local")

        # Set a timer for the next plot
        self.timer = threading.Timer(10, self.plot_heatmap)
        self.timer.start()