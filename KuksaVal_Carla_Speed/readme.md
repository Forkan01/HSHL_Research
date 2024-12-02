# A. Steps to Get Started:
## 1. Clone the Kuksa.val Repository:
Open a terminal and run the following command to clone the Kuksa.valrepository from GitHub:

- git clone https://github.com/eclipse/kuksa.val.git
- cd kuksa.val

## 2. Build and Run the Kuksa.valServer:
- Open Docker
- In Terminal:
  docker-compose up --build

### [ Helpfull:
3. Check your running containers by:
- docker ps
Inspect the server logs:
- docker logs <container_id>

4. Check Server Ports:
Verify that the server is listening on the expected port (e.g., 55555)
- netstat -an | findstr 55555

5. Use the Kuksa.valCLI:
You can interact with the server using the Kuksa.valCLI to check for data points.
- docker run -it --rm --net=host ghcr.io/eclipse/kuksa.val/databroker-cli:master 

Example commands to verify data points:
- get Vehicle.Speed
- feed Vehicle.Speed 200
- quit      ]

# B. Execution:
## 1. The 'Direct' folder contains the all in one file, which can directly get the vehicle speed within the code.
   
## 2. The other three files as based on server-client system.
- Create 3 terminals
- 1st open the 'speed_provider.py'
- 2nd open the original 'manual_control.py' file. (keep Carla on beforehand)
- 3rd open the 'speed_fetcher
