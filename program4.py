
import time

print("Connecting...")
time.sleep(2)
print("Connected")
time.sleep(2)
print("ARMED")

time.sleep(2)
print("Takeoff")

time.sleep(2)
print("Reached target altitude")

time.sleep(2)
print("Mode: LOITER")
time.sleep(10)
print("Due to low Battery, switching to LAND mode")

time.sleep(3)
print("Mode: LAND")

time.sleep(2)
print("landing...")

time.sleep(2)
print("DISARMED")