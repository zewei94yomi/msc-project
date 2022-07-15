import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
from commons.configuration import NOISE_BASE_PATH, HEATMAP_BASE_PATH, OVERLAY_BASE_PATH, GEO_PATH, PD_PATH, CRS
from commons.configuration import MAP_LEFT, MAP_BOTTOM, MAP_TOP, MAP_RIGHT
from commons.configuration import style_function, highlight_function
import os
from folium.raster_layers import ImageOverlay


def create_map(popup, population_density, threshold_scale, x_center, y_center):
    mymap = folium.Map(location=[y_center, x_center], zoom_start=13)
    folium.TileLayer('CartoDB positron', name="Light Map", control=False).add_to(mymap)
    folium.Choropleth(
        geo_data=popup,
        name='Choropleth',
        data=population_density,
        columns=['tract', 'Population_Density_in_2010'],
        key_on="properties.id2",
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        threshold_scale=threshold_scale,
        legend_name='Population Density',
        smooth_factor=0
    ).add_to(mymap)
    
    NIL = folium.features.GeoJson(
        popup,
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
    return mymap


def add_heatmap(trajectory, mymap):
    heatmap = HeatMap(trajectory, radius=15, min_opacity=1)
    mymap.add_child(heatmap)
    mymap.keep_in_front(heatmap)
    return mymap


def visualize_heatmap(geo, pd_data, popup):
    threshold_scale = list(pd_data["Population_Density_in_2010"].quantile([0, 0.2, 0.4, 0.6, 0.8, 1]))
    x_center = geo.to_crs(CRS).centroid.to_crs(geo.crs).x.mean()
    y_center = geo.to_crs(CRS).centroid.to_crs(geo.crs).y.mean()
    directory_path = "../" + NOISE_BASE_PATH
    for filename in os.listdir(directory_path):
        mymap = create_map(popup=popup,
                           population_density=pd_data,
                           threshold_scale=threshold_scale,
                           x_center=x_center,
                           y_center=y_center)
        file_path = directory_path + "/" + filename
        noise_df = pd.read_csv(file_path).drop(columns=['Time Slice'])
        print(f"Done loading noise data from \'{filename}.csv\'")
        noise_df = noise_df.sort_values(by=['Noise'])
        noise_list = noise_df.values.tolist()
        add_heatmap(trajectory=noise_list, mymap=mymap)
        html_path = "../" + HEATMAP_BASE_PATH + "/folium/" + filename + ".html"
        mymap.save(html_path)
        print(f"Done saving noise heatmap to \'{filename}.html\'")
        
        
def visualize_matrix(geo, pd_data, popup):
    threshold_scale = list(pd_data["Population_Density_in_2010"].quantile([0, 0.2, 0.4, 0.6, 0.8, 1]))
    x_center = geo.to_crs(CRS).centroid.to_crs(geo.crs).x.mean()
    y_center = geo.to_crs(CRS).centroid.to_crs(geo.crs).y.mean()
    directory_path = "../" + HEATMAP_BASE_PATH + "/matplotlib"
    max_path = directory_path + '/maximum'
    average_path = directory_path + '/average'
    # saving maximum
    for filename in os.listdir(max_path):
        mymap = create_map(popup=popup,
                           population_density=pd_data,
                           threshold_scale=threshold_scale,
                           x_center=x_center,
                           y_center=y_center)
        max_file_path = max_path + "/" + filename
        average_file_path = average_path + "/" + filename
        ImageOverlay(max_file_path,
                     [[MAP_BOTTOM * 0.9998, MAP_LEFT * 1.00018], [MAP_TOP * 1.00015, MAP_RIGHT * 0.99955]],
                     name='maximum',
                     opacity=0.8,
                     ).add_to(mymap)
        ImageOverlay(average_file_path,
                     [[MAP_BOTTOM * 0.9998, MAP_LEFT * 1.00018], [MAP_TOP * 1.00015, MAP_RIGHT * 0.99955]],
                     name='average',
                     opacity=0.8,
                     ).add_to(mymap)
        folium.LayerControl().add_to(mymap)
        html_path = "../" + OVERLAY_BASE_PATH + "/" + filename.split('.')[0] + ".html"
        print(f"Done loading density matrix")
        mymap.save(html_path)
        print(f"Done saving overlay image to \'{filename}.html\'")
        

if __name__ == '__main__':
    geo = gpd.read_file("../" + GEO_PATH)
    pd_data = pd.read_csv("../" + PD_PATH)
    popup = geo.merge(pd_data, left_on="id2", right_on="tract")
    # visualize_heatmap(geo, pd_data, popup)
    visualize_matrix(geo, pd_data, popup)
