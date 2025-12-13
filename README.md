# Smart Study Spot

## Project overview
Smart Study Spot is an Internet of Things (IoT) project developed to monitor and visualize the real-time occupancy of shared study desks on campus. The sstem uses multiple low-cost sensors connected to a Raspberry Pi to determine whether a desk is occupied and publishes this information to a cloud platform for visualization.

The goal of the project is to help students easily find available study spaces and to provide administratos with data about space usage. This projectt was developed as part of the Internet of Things Application Development course in the Bachelor's Degree program at the University of Deusto.

## System description
The system monitors the occupancy of two study desks, each one equipped with three different sensors:
  * Distance sensor (ultrasonic): detects the presence os a person in front of the desk.
  * Light sensor: detects desk activity such as a laptop screen or desk lamp.
  * Pressure sensor (button): placed on the chair and activated when someone sits down.

Sensor data is processed locally on a Raspberry Pi using a simple sensor-fusion logic. If at least two out of three sensors indicate activity, the desk is considered occupied.

The occupancy status is sent using MQTT-compatible cloud infrastructure and stored in InfluxDB, while Grafana is used to visualize the data in real time.

## Occupancy logic
For each desk:
- Each sensor produces a boolean value (active/inactive).
- The desk state is calculated as:
 - occupied = true if at least 2 sensors are active.
 - occupied = false otherwise.

This approach increases reliability compared to using a single sensor and helps reduce false positives and negatives.

## System architecture
Sensing layer
    * Grove light sensor
    * Grove ultrasonic distance sensor
    * Grove button (pressure sensor)

Edge processing
    * Raspberry Pi
    * Python script with multithreading (one thread per desk)

Data and communication layer
    * InfluxDB Cloud (tme-series database)
    * MQTT-based data publishing (via InfluxDB client)

Application layer
    * Grafana dashboard
    * Real-time desk occupancy visualization

Data flow
    Sensor --> Raspberry Pi (local logic) --> InfluxDB cloud --> Grafana dashboard

## Technologies used
* Python 3
* Raspberry Pi
* Grove Base Kit
* RPi.GPIO
* InfluxDB Cloud
* Grafana
* MQTT
* Multithreading

## How to run the project
### Requirements
* Raspberry Pi with Raspberry Pi OS
* Grove base hat
* Grove light sensors
* Grove ultrasonic sensors
* Grove buttons
* Python 3

### Python dependencies 
Install required libraries:
`pip install influxdb-client grove.py`

### Configuration
1. Connect the sensor to the Raspberry Pi:
   * Light sensors to analog ports (A0 and A2)
   * Ultrasonic sensors to digital ports (D16 and D18)
   * Buttons to GPIO pins (D24 and D26)
2. Update the InfluxDB configuration in the script:
   * url
   * token
   * org
   * bucket

### Execution
Run the script:
`python hilo.py`
The script continuously reads sensor data every second and updates the occupancy state for each desk.

## Dashboard
The Grafana dashboard displays:
* Real-time occupancy status of each desk
* Historical occupancy data
* Time-based usage patterns

## Project status
This project represents a functional MVP (Minimum Viable Product) developed for academic purposes.

## Authors
Natalia, Naroa and Telmo







