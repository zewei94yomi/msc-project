# 1. Overview

- Order Generator is used to simulate the process of generating new food delivery orders.

- Order Generator will automatically generate food delivery orders based on population density (PD) on a map. Areas with high PD are more likely to generate food delivery orders, while areas with low PD are less likely to generate food delivery orders.

- According to OOP's principles, Order Generator will only generate orders. 

- TODO: These orders will be either accepted by drones or allocated by central processor.





# 2. Requirements

## a. Fixed Area

Orders will be generated in a fixed area. Coordinates will be represented by using longitude and latitude. Users will need to input four coordinates of the fixed area.


## b. Population Density

The program should be able to read population density data.


## c. Generate Orders

Orders can be generated before the program/simulation starts or generated gradually. 



## d. Orders & Population Density

Orders should be generated according to population density or randomly.

### Restaurant

There is no data for every restaurant's location in San Francisco, therefore orders' start location (i.e. Restaurant):
1. Generate restaurants clusters based on population density
2. Random

### Customer

The order destinations or customer locations should be generated based on population density


# 3. Data

## a. Map/Area

- Boundary
  - Top left (Coordinate)
  - Top right (Coordinate)
  - Bottom left (Coordinate)
  - Bottom right (Coordinate)
- `TODO`: Population density 



## c. Coordinate

- Longitude
- Latitude



## b. Order

- uid

- Time

- Start (Coordinate)

- End (Coordinate)

## c. Density
Population density

- TODO