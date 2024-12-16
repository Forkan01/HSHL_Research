import carla
import time
from kuksa_client.grpc import VSSClient, Datapoint

def get_vehicle_speed(vehicle):
    velocity = vehicle.get_velocity()
    speed = (velocity.x**2 + velocity.y**2 + velocity.z**2)**0.5  # Calculate speed
    return speed

def main():
    # Set up CARLA client
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()

    # Wait for a vehicle to appear in the simulation
    while True:
        vehicles = world.get_actors().filter('vehicle.*')
        if len(vehicles) > 0:
            vehicle = vehicles[0]
            break
        print("Waiting for vehicle to spawn...")
        time.sleep(1)

    # Connect to Kuksa.val server
    with VSSClient('127.0.0.1', 55555) as kuksa_client:
        while True:
            speed = get_vehicle_speed(vehicle)
            kuksa_client.set_current_values({'Vehicle.Speed': Datapoint(speed)})
            print(f'Feeding Vehicle.Speed: {speed:.2f}')
            time.sleep(1)

if __name__ == "__main__":
    main()
