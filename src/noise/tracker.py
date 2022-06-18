from commons.decorators import auto_str
from drones.drone import Drone


@auto_str
class NoiseTracker:
    
    def __init__(self):
        self.noise = list()
        self.min_noise = float('inf')
        self.max_noise = float('-inf')

    def track_noise(self, drone: Drone):
        la = drone.current_location.latitude
        lo = drone.current_location.longitude
        noise = drone.produce_noise()
        self.max_noise = max(self.max_noise, noise)
        self.min_noise = min(self.min_noise, noise)
        self.noise.append([la, lo, noise])
    
    # def plot_heatmap(self):
    #     # Create a map
    #     m = folium.Map(
    #         location=[37.7629, -122.4394],  # [latitude, longitude]
    #         zoom_start=13,
    #         tiles='stamentoner')
    #
    #     # Read geo data
    #     with open("recourses/shown_geography.geojson") as f:
    #         sf_geo = json.load(f)
    #
    #     # Read population density data
    #     sf_data = pd.read_csv("recourses/shown_tract_popdensity2010.csv")
    #
    #     bins = list(sf_data["Population_Density_in_2010"].quantile([0, 0.2, 0.4, 0.6, 0.8, 1]))
    #
    #     # Plot choropleth on the map
    #     folium.Choropleth(
    #         geo_data=sf_geo,
    #         name="choropleth",
    #         data=sf_data,
    #         columns=["tract", "Population_Density_in_2010"],
    #         key_on="properties.id2",
    #         fill_color="YlOrRd",
    #         fill_opacity=0.7,
    #         line_opacity=0.2,
    #         bins=bins,
    #         # highlight=True,
    #         legend_name="Population Density p/mi",
    #     ).add_to(m)
    #
    #     # Plot noise heatmap
    #     heatmap = HeatMap(self.noise, radius=15)
    #     m.add_child(heatmap)
    #     # m.keep_in_front(heatmap)  # TODO: 还是没法解决层级叠加问题
    #
    #     # Open latitude and longitude popup
    #     m.add_child(folium.LatLngPopup())
    #
    #     # Open layer control
    #     folium.LayerControl().add_to(m)
    #
    #     # Save the heatmap
    #     now = datetime.now()
    #     name = now.strftime("%m-%d_%H-%M-%S")
    #     m.save('noise/HeatMaps/' + name + '.html')  # 保存为HTML
    #     print("New heatmap has been saved to local")
    #
    #     # Set a timer for the next plot
    #     self.timer = threading.Timer(10, self.plot_heatmap)
    #     self.timer.start()
    #
    # def plot_heatmap_2(self):
    #     geo = gpd.read_file("recourses/shown_geography.geojson")
    #     data = pd.read_csv('recourses/shown_tract_popdensity2010.csv')
    #     pop = geo.merge(data, left_on="id2", right_on="tract")
    #     x_map = geo.centroid.x.mean()
    #     y_map = geo.centroid.y.mean()
    #     mymap = folium.Map(location=[y_map, x_map], zoom_start=13, tiles=None)
    #     folium.TileLayer('CartoDB positron', name="Light Map", control=False).add_to(mymap)
    #     myscale = list(data["Population_Density_in_2010"].quantile([0, 0.2, 0.4, 0.6, 0.8, 1]))
    #     mymap.choropleth(
    #         geo_data=geo,
    #         name='Choropleth',
    #         data=data,
    #         columns=['tract', 'Population_Density_in_2010'],
    #         key_on="properties.id2",
    #         fill_color='YlGnBu',
    #         threshold_scale=myscale,
    #         fill_opacity=1,
    #         line_opacity=0.2,
    #         legend_name='Population Density',
    #         smooth_factor=0
    #     )
    #
    #     style_function = lambda x: {'fillColor': '#ffffff',
    #                                 'color': '#000000',
    #                                 'fillOpacity': 0.1,
    #                                 'weight': 0.1}
    #     highlight_function = lambda x: {'fillColor': '#000000',
    #                                     'color': '#000000',
    #                                     'fillOpacity': 0.50,
    #                                     'weight': 0.1}
    #
    #     NIL = folium.features.GeoJson(
    #         pop,
    #         style_function=style_function,
    #         control=False,
    #         highlight_function=highlight_function,
    #         tooltip=folium.features.GeoJsonTooltip(
    #             fields=['tract', 'Name', 'Population_Density_in_2010'],
    #             aliases=['Tract: ', 'Name: ', 'Population Density (people in per sq mi): '],
    #             style="background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"
    #         )
    #     )
    #     mymap.add_child(NIL)
    #     mymap.keep_in_front(NIL)
    #
    #     # Plot noise heatmap
    #     heatmap = HeatMap(self.noise, radius=15)
    #     mymap.add_child(heatmap)
    #
    #     folium.LayerControl().add_to(mymap)
    #     # Save the heatmap
    #     now = datetime.now()
    #     name = now.strftime("%m-%d_%H-%M-%S")
    #     mymap.save('noise/HeatMaps/' + name + '.html')  # 保存为HTML
    #     print("New heatmap has been saved to local")
    #
    #     # Set a timer for the next plot
    #     self.timer = threading.Timer(10, self.plot_heatmap_2)
    #     self.timer.start()
    #
    # def rescale_noise(self):
    #     # TODO
    #     return [[x[0], x[1], (x[2] - self.min_noise) / (self.max_noise - self.min_noise)] for x in self.noise]
    #
    #

