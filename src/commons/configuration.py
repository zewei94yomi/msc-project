# Print on the terminal
PRINT_TERMINAL = True
# Plot the simulation
PLOT_SIMULATION = True
# Use DensityMatrix to track noise: tracking noise in matrix
USE_DENSITY_MATRIX = True
# Use local order data; otherwise generate new orders
USE_LOCAL_ORDER = True
# Prioritize to low-average-noise cells, i.e. prioritize fairness
PRIORITIZE_K = 50
# Use NoiseTracker to track noise (DEPRECATED: default to be False)
USE_NOISE_TRACKER = False
# Consider population density in A* search
USE_POPULATION_DENSITY = False
# Save noise trajectory data to local in csv; need to use NoiseTracker
SAVE_CSV = True

# Coordinates of warehouses
WAREHOUSES = [[37.805858377440266, -122.41276123169143],
              [37.76077744044274, -122.390011845567],
              [37.7426674419608, -122.39981393102507]]
# Total number of orders
ORDERS = 30
# Total number of drones
DRONES = 10

# Noise matrix cell size (in meter)
NOISE_CELL_LENGTH = 100
NOISE_CELL_WIDTH = 100
# Used in 'Tracker' for radiating noise, the radius for radiation will be NOISE_CELL_LENGTH * NOISE_CELL_NUM
NOISE_CELL_NUM = 5
# The minimum noise level that the tracker will store, e.g. if the mixed noise is 39db, then it will be ignored
TRACK_NOISE_THRESHOLD = 40

# The number of iterations that a tracker will write noise data to the local
# e.g. TRACKER_ITERATIONS = 20, the program will run 20 iterations
# and save noise data to the local and clean the memory
TRACKER_ITERATIONS = 10

# Center iteration running step
# e.g. CENTER_PER_SLICE_TIME = 1s, the program will run each iteration for 0.5 second (if possible)
# when it's the iteration to writing data to local, the program will slow down a little bit,
# but it will run faster in the next a few iterations to compensate for the slow-down
CENTER_PER_SLICE_TIME = 0.5

# Path
# Base path for saving/loading orders to/from the local
ORDER_BASE_PATH = 'recourses/data/order/orders.csv'
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
# Base path for saving noise histogram
HISTOGRAM_BASE_PATH = 'recourses/results/noise/histogram'
# Base path for experiment results
RESULT_BASE_PATH = 'recourses/results/experiments'

# Map
CRS = 'epsg:3857'
# Map boundary
MAP_LEFT = -122.520
MAP_RIGHT = -122.375
MAP_TOP = 37.820
MAP_BOTTOM = 37.700
# offset 0-200m (latitude) to a random generated coordinate
RANDOM_LA_COORD_OFFSET = 0.001802
# offset 0-200m (longitude) to a random generated coordinate
RANDOM_LO_COORD_OFFSET = 0.002278

# geo popup layer style and highlight functions
style_function = lambda x: {'fillColor': '#ffffff',
                            'color': '#000000',
                            'fillOpacity': 0.1,
                            'weight': 0.1}
highlight_function = lambda x: {'fillColor': '#000000',
                                'color': '#000000',
                                'fillOpacity': 0.50,
                                'weight': 0.1}