import pandas as pd
import numpy as np
from commons.configuration import RESULT_BASE_PATH
from commons.my_util import plot_matrix, plot_histogram
from commons.configuration import GEO_PATH, PD_PATH, CRS
from commons.configuration import style_function, highlight_function
from commons.configuration import HARM_AVG_LEVEL, HARM_MAX_LEVEL
import geopandas as gpd
import folium
from folium.raster_layers import ImageOverlay
import csv
import seaborn as sns
from matplotlib import pyplot as plt

# directory name: e.g. 'p=5', '2022-07-22_18:00:00'
directory = '08-06_16:46:48'

# concat the path
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
plot_matrix(X, Y, avg_noises, avg_title, result_path + '/avg_matrix', color_min=25, color_max=60)
plot_matrix(X, Y, max_noises, max_title, result_path + '/max_matrix', color_min=40, color_max=105)

# average/maximum harm map
avg_noises_harm = np.array(avg_noises)
max_noises_harm = np.array(max_noises)
cnt_avg_harm_cell = 0
cnt_max_harm_cell = 0
cnt_100_harm_cell = 0
for i in range(rows):
    for j in range(cols):
        if avg_noises_harm[i][j] - HARM_AVG_LEVEL >= 0:
            cnt_avg_harm_cell += 1
        else:
            avg_noises_harm[i][j] = 0
        if max_noises_harm[i][j] - HARM_MAX_LEVEL >= 0:
            cnt_max_harm_cell += 1
        else:
            max_noises_harm[i][j] = 0
        if max_noises_harm[i][j] >= 100:
            cnt_100_harm_cell += 1
avg_harm_title = f"Average Noise Harm Matrix (>{HARM_AVG_LEVEL}db)"
max_harm_title = f"Maximum Noise Harm Matrix (>{HARM_MAX_LEVEL}db)"
plot_matrix(X, Y, avg_noises_harm, avg_harm_title, result_path + '/avg_harm_matrix', color_min=0, color_max=55)
plot_matrix(X, Y, max_noises_harm, max_harm_title, result_path + '/max_harm_matrix', color_min=0, color_max=105)

print(f"Number of cells over avg harm threshold: {cnt_avg_harm_cell}, {round(cnt_avg_harm_cell/(rows * cols) * 100, 3)}%")
print(f"Number of cells over max harm threshold: {cnt_max_harm_cell}, {round(cnt_max_harm_cell/(rows * cols) * 100, 3)}%")
print(f"Number of cells over 100 db: {cnt_100_harm_cell}, {round(cnt_100_harm_cell/(rows * cols) * 100, 3)}%")

# 3. overlay images on folium
geo = gpd.read_file('../' + GEO_PATH)
pd_data = pd.read_csv('../' + PD_PATH)
popup = geo.merge(pd_data, left_on="id2", right_on="tract")
threshold_scale = list(pd_data["Population_Density_in_2010"].quantile([0, 0.2, 0.4, 0.6, 0.8, 1]))
x_center = geo.to_crs(CRS).centroid.to_crs(geo.crs).x.mean()
y_center = geo.to_crs(CRS).centroid.to_crs(geo.crs).y.mean()

mymap = folium.Map(location=[y_center, x_center], zoom_start=13)
# folium.TileLayer('CartoDB positron', name="Light Map", control=False).add_to(mymap)
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
    legend_name='Population Density (number of people per square mile)',
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
avg_harm_img_path = result_path + '/avg_harm_matrix.png'
max_harm_img_path = result_path + '/max_harm_matrix.png'
max_overlay = ImageOverlay(max_img_path,
                           [[config['Bottom Latitude'] * 0.9998 - 0.001, config['Left Longitude'] * 1.00018 - 0.006],
                            [config['Top Latitude'] * 1.00025 - 0.001, config['Right Longitude'] * 0.99952 - 0.004]],
                           name='maximum',
                           opacity=1,
                           )
avg_overlay = ImageOverlay(avg_img_path,
                           [[config['Bottom Latitude'] * 0.9998 - 0.001, config['Left Longitude'] * 1.00018 - 0.006],
                            [config['Top Latitude'] * 1.00025 - 0.001, config['Right Longitude'] * 0.99952 - 0.004]],
                           name='average',
                           opacity=1,
                           )
avg_harm_overlay = ImageOverlay(avg_harm_img_path,
                           [[config['Bottom Latitude'] * 0.9998 - 0.001, config['Left Longitude'] * 1.00018 - 0.006],
                            [config['Top Latitude'] * 1.00025 - 0.001, config['Right Longitude'] * 0.99952 - 0.004]],
                           name='average_harm',
                           opacity=0.8,
                           )
max_harm_overlay = ImageOverlay(max_harm_img_path,
                           [[config['Bottom Latitude'] * 0.9998 - 0.001, config['Left Longitude'] * 1.00018 - 0.006],
                            [config['Top Latitude'] * 1.00025 - 0.001, config['Right Longitude'] * 0.99952 - 0.004]],
                           name='maximum_harm',
                           opacity=0.8,
                           )
mymap.add_child(max_overlay)
mymap.add_child(avg_overlay)
mymap.add_child(avg_harm_overlay)
mymap.add_child(max_harm_overlay)
folium.LayerControl().add_to(mymap)
html_path = result_path + '/overlay.html'
mymap.save(html_path)


# 4. maximum histogram
# 5. average histogram
sns.set_style('whitegrid')
plt.ylim((0, 1000))
plot_histogram(data=matrix_df['Average Noise'],
               title='Average',
               path=result_path + '/avg_histogram',
               y_bottom=0,
               y_top=1600)
plt.ylim((0, 10000))
plot_histogram(data=matrix_df['Maximum Noise'],
               title='Maximum',
               path=result_path + '/max_histogram',
               y_bottom=0,
               y_top=12500)


# 6*. fairness
total_drones = drone_df['Total Distance'].count()
total_distance = drone_df['Total Distance'].sum()
total_orders = drone_df['Total Orders'].sum()
total_noise = matrix_df['Average Noise'].sum() * iterations
avg_distance = total_distance / total_orders
max_noise = matrix_df['Average Noise'].max()
mean_noise = matrix_df['Average Noise'].mean()
quantile_25_noise = matrix_df['Average Noise'].quantile(0.25)
quantile_50_noise = matrix_df['Average Noise'].quantile(0.50)   # median
quantile_75_noise = matrix_df['Average Noise'].quantile(0.75)


fairness_fields = ['Total Drones', 'Total Orders', 'Total Distance', 'Total Noise',
                   'Order Average Distance', 'std dev', 'Maximum Average Noise', 'Mean Average Noise', '25% Quantiles', '50% Quantiles', '75% Quantiles', 'Priority']
fairness_data = [[total_drones, total_orders, total_distance, total_noise,
                  avg_distance, std, max_noise, mean_noise, quantile_25_noise, quantile_50_noise, quantile_75_noise, config['Prioritization K']]]
fairness_path = result_path + '/fairness.csv'
with open(fairness_path, 'w') as f:
    write = csv.writer(f)
    write.writerow(fairness_fields)
    write.writerows(fairness_data)
    f.flush()
    f.close()
