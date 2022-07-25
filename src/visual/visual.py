import pandas as pd
import numpy as np
from commons.configuration import RESULT_BASE_PATH
from commons.my_util import plot_pcolormesh, plot_histogram
from commons.configuration import GEO_PATH, PD_PATH, CRS
from commons.configuration import style_function, highlight_function
import geopandas as gpd
import folium
from folium.raster_layers import ImageOverlay
import csv
import seaborn as sns

# file path
directory = '07-24_18:18:25'
result_path = '../' + RESULT_BASE_PATH + '/' + directory

# read data
matrix_df = pd.read_csv(result_path + '/matrix.csv')
config_df = pd.read_csv(result_path + '/config.csv')
drone_df = pd.read_csv(result_path + '/drone.csv')

# 1. maximum density matrix image
# 2. average density matrix image
config = config_df.iloc[0]
rows = int(config['Rows'])
cols = int(config['Cols'])
la = np.linspace(config['Top Latitude'], config['Bottom Latitude'], rows)
lo = np.linspace(config['Left Longitude'], config['Right Longitude'], cols)
avg_noises = matrix_df['Average Noise'].to_numpy().reshape(rows, cols)
max_noises = matrix_df['Maximum Noise'].to_numpy().reshape(rows, cols)
std = np.std(avg_noises)
iterations = int(matrix_df.iloc[0]['Time'])
X, Y = np.meshgrid(lo, la)
avg_title = f"Average Noise Matrix in {iterations} iterations"
max_title = f"Maximum Noise Matrix in {iterations} iterations"
plot_pcolormesh(X, Y, avg_noises, avg_title, result_path + '/avg_matrix')
plot_pcolormesh(X, Y, max_noises, max_title, result_path + '/max_matrix')

# 3. overlay image on folium
geo = gpd.read_file('../' + GEO_PATH)
pd_data = pd.read_csv('../' + PD_PATH)
popup = geo.merge(pd_data, left_on="id2", right_on="tract")
threshold_scale = list(pd_data["Population_Density_in_2010"].quantile([0, 0.2, 0.4, 0.6, 0.8, 1]))
x_center = geo.to_crs(CRS).centroid.to_crs(geo.crs).x.mean()
y_center = geo.to_crs(CRS).centroid.to_crs(geo.crs).y.mean()

mymap = folium.Map(location=[y_center, x_center], zoom_start=13)
folium.TileLayer('CartoDB positron', name="Light Map", control=False).add_to(mymap)
folium.Choropleth(
    geo_data=popup,
    name='Choropleth',
    data=pd_data,
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

max_img_path = result_path + '/max_matrix.png'
avg_img_path = result_path + '/avg_matrix.png'
max_overlay = ImageOverlay(max_img_path,
                           [[config['Bottom Latitude'] * 0.9998, config['Left Longitude'] * 1.00018],
                            [config['Top Latitude'] * 1.00015, config['Right Longitude'] * 0.99955]],
                           name='average',
                           opacity=0.8,
                           )
avg_overlay = ImageOverlay(avg_img_path,
                           [[config['Bottom Latitude'] * 0.9998, config['Left Longitude'] * 1.00018],
                            [config['Top Latitude'] * 1.00015, config['Right Longitude'] * 0.99955]],
                           name='maximum',
                           opacity=0.8,
                           )
mymap.add_child(max_overlay)
mymap.add_child(avg_overlay)
folium.LayerControl().add_to(mymap)
html_path = result_path + '/overlay.html'
mymap.save(html_path)


# 4. maximum histogram
# 5. average histogram
# sns.set_style('darkgrid')
sns.set_style('whitegrid')
plot_histogram(data=matrix_df['Average Noise'], title='Average', path=result_path + '/avg_histogram')
plot_histogram(data=matrix_df['Maximum Noise'], title='Maximum', path=result_path + '/max_histogram')


# 6*. fairness
total_drones = drone_df['Total Distance'].count()
total_steps = drone_df['Total Step'].sum()
total_distance = drone_df['Total Distance'].sum()
total_orders = drone_df['Total Orders'].sum()
total_noise = matrix_df['Average Noise'].sum() * iterations
avg_distance = total_distance / total_orders
max_noise = matrix_df['Average Noise'].max()
mean_noise = matrix_df['Average Noise'].mean()
quantile_25_noise = matrix_df['Average Noise'].quantile(0.25)
quantile_50_noise = matrix_df['Average Noise'].quantile(0.50)   # median
quantile_75_noise = matrix_df['Average Noise'].quantile(0.75)


fairness_fields = ['Total Drones', 'Total Orders', 'Total Distance', 'Total Step', 'Total Noise',
                   'Order Average Distance', 'std dev', 'Maximum Average Noise', 'Mean Average Noise', '25% Quantiles', '50% Quantiles', '75% Quantiles', 'Priority']
fairness_data = [[total_drones, total_orders, total_distance, total_steps, total_noise,
                  avg_distance, std, max_noise, mean_noise, quantile_25_noise, quantile_50_noise, quantile_75_noise, config['Prioritization K']]]
fairness_path = result_path + '/fairness.csv'
with open(fairness_path, 'w') as f:
    write = csv.writer(f)
    write.writerow(fairness_fields)
    write.writerows(fairness_data)
    f.flush()
    f.close()
