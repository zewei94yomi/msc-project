import pandas as pd
import plotly.graph_objects as go
from commons.configuration import NOISE_BASE_PATH, HEATMAP_BASE_PATH
import os


directory_path = "../" + NOISE_BASE_PATH

for filename in os.listdir(directory_path):
    file_path = directory_path + "/" + filename
    noise_df = pd.read_csv(file_path)
    print(f"Done loading noise data from \'{filename}.csv\'")
    noise_df = noise_df.sort_values(by=['Noise']).drop(columns=['Time Slice'])
    fig = go.Figure(go.Densitymapbox(lat=noise_df.Latitude, lon=noise_df.Longitude, z=noise_df.Noise,
                                     radius=10))
    fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=180)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    html_path = "../" + HEATMAP_BASE_PATH + "/ploty/" + filename + ".html"
    fig.write_html(html_path)
    print(f"Done saving noise heatmap to \'{filename}.html\'")






