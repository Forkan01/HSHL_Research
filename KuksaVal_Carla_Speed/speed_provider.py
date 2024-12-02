import carla
import time
import socket

# Configuration
HOST = '127.0.0.1'  # Localhost
PORT = 55555        # Port to listen on

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

    # Set up server to provide vehicle speed
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Speed provider server started on {HOST}:{PORT}')
        conn, addr = s.accept()
        with conn:
            print(f'Connected by {addr}')
            while True:
                speed = get_vehicle_speed(vehicle)
                conn.sendall(f'{speed:.2f}'.encode())
                time.sleep(1)

if __name__ == "__main__":
    main()
