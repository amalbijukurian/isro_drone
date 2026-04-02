from pymavlink import mavutil
import time

PORT = "/dev/ttyACM0"
BAUD = 115200

print("Connecting...")
master = mavutil.mavlink_connection(PORT, baud=BAUD)
master.wait_heartbeat()
print("Connected")

time.sleep(2)
print("\nARMED\n")

time.sleep(2)
print("Takeoff")

time.sleep(2)
print("Reached target altitude")

time.sleep(2)
print("Mode: LOITER")

time.sleep(2)
print("Mode: LAND")

time.sleep(2)
print("landing...")

time.sleep(2)
print("DISARMED")