# Print on the terminal
PRINT_TERMINAL = False
# Plot the simulation
PLOT_SIMULATION = True
# Use NoiseTracker to track noise
USE_TRACKER = False
# Save noise trajectory data to local in csv; need to use tracker
SAVE_CSV = True
# Use DensityMatrix to track noise: track noise in matrix and plot data
USE_MATRIX = True

# Noise matrix cell size (meter)
NOISE_CELL_LENGTH = 80
NOISE_CELL_WIDTH = 80
# Used in 'Tracker' for radiating noise
NOISE_CELL_NUM = 5
# The minimum noise level that the tracker will store, e.g. if the mixed noise is 39db, then it will be ignored
TRACK_NOISE_THRESHOLD = 40

# Noise Tracker & Density Matrix
# The number of rounds that a tracker will save noise data to local
# e.g. TRACKER_TIME_SLICE = 20, the program will run 20 iterations
# and save noise data to local and clear them from the memory
TRACKER_TIME_SLICE = 10

# Center iteration running time
# e.g. CENTER_PER_SLICE_TIME = 1s, the program will run each iteration for 0.5 second
# when it's time to writing data to local, the program will slow down a little bit, but it will run faster in the next
# a few iterations to compensate for the slow-down
CENTER_PER_SLICE_TIME = 1


# Path
# Base path for saving/loading noise tracking data
NOISE_BASE_PATH = 'recourses/results/noise/trajectory'
# Base path for saving heatmap/density map
HEATMAP_BASE_PATH = 'recourses/results/noise/heatmaps'
# Base path for saving overlay images of folium map and density matrix
OVERLAY_BASE_PATH = 'recourses/results/noise/heatmaps/overlay'
# Geographical data
GEO_PATH = 'recourses/data/geo/shown_geography.geojson'
# Population density data
PD_PATH = 'recourses/data/population/shown_tract_popdensity2010.csv'
# Simulation plotter background image
BACKGROUND_IMAGE_PATH = 'recourses/images/map.jpeg'
# Base path for saving noise density matrix
MATRIX_BASE_PATH = 'recourses/results/noise/matrix'

# Map
CRS = 'epsg:3857'
MAP_LEFT = -122.520
MAP_RIGHT = -122.375
MAP_TOP = 37.820
MAP_BOTTOM = 37.700
# offset 200m (latitude) to the random generated coordinate
RANDOM_LA_COORD_OFFSET = 0.001802
RANDOM_LO_COORD_OFFSET = 0.002278

# Coordinates of warehouses
WAREHOUSES = [[37.751800, -122.478555], [37.72, -122.428], [37.78, -122.39]]
# Total number orders
ORDERS = 10
# Total number of drones
DRONES = 10

# geo popup layer style and highlight functions
style_function = lambda x: {'fillColor': '#ffffff',
                            'color': '#000000',
                            'fillOpacity': 0.1,
                            'weight': 0.1}
highlight_function = lambda x: {'fillColor': '#000000',
                                'color': '#000000',
                                'fillOpacity': 0.50,
                                'weight': 0.1}