# 1. Overview

- Order Generator is used to producing new food delivery orders.

- Orders will be produced either:
   - Randomly
   - Based on population density
   
- New orders will be sent to the order center

- Since the aim of this project is to simulate the process of drone food delivery, complex design patterns such as observer pattern will not be considered to implement.

# 2. Requirements

## a. Fixed Area

The order generator should be able to generate orders in a fixed area. The fixed area will be represented by a `Map` instance.

## b. Population Density

The order generator should be able to generate orders based on population density, e.g. areas with high PD are more likely to generate food delivery orders, while areas with low PD are less likely to generate food delivery orders.

## c. Generate Orders

The order generator should be able to generate orders before the program/simulation starts and send them to the order center. 

# 3. Data
### Restaurant

There is no data for restaurants' location in San Francisco, therefore we have two strategies for generating orders' start location (i.e. Restaurant):
1. Generate clusters based on population density (Based on an assumption that the number of restaurants has 
   positive relation with the population density)
2. Random

### Customer

Customers' locations (i.e. order destinations) should be generated based on population density

# 4. Field

- map: Map

# 5. API

1. Generate order
   ```python
   generate_order(self, use_density=False)
   ```
   Generate an `Order` on the given map. The order will be randomly generated if 
   the argument `use_density` is `False`, otherwise the order is generated based on 
   population density