# About 
This project is a King's College London MSc Individual Project (7CCSMPRJ). The name of the project is 'Modeling and Reducing Noise in Drone Delivery
Fleets'. The software is developed to simulate a drone food delivery system. 

There is similar simulation software written in Julia: https://github.com/sisl/MultiAgentAllocationTransit.jl

# How to run

1. Install required packages
    ```bash
    pip install -r requirements.txt
    ```

2. Configure simulation settings. You can set the number of orders, number of drones, locations of warehouses, prioritizing factor K or P and size of cells in `src/commons/configurations.py`

3. Run the application in `src/application.py`

# Simulation

![Simulation](https://github.com/zewei94yomi/msc-project/blob/master/src/recourses/images/delivery.gif)