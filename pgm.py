from pymavlink import mavutil
import time

TARGET_ALT = 4.0

PORT = "/dev/ttyACM0"
BAUD = 115200

print("Connecting to MAVLink...")
master = mavutil.mavlink_connection(PORT, baud=BAUD)
master.wait_heartbeat()
print("Connected")

armed_printed = False
takeoff_printed = False
target_printed = False
loiter_printed = False
land_printed = False

while True:

    msg = master.recv_match(blocking=True)

    if not msg:
        continue

    # -------------------------
    # ARM / DISARM detection
    # -------------------------
    if msg.get_type() == "HEARTBEAT":

        armed = master.motors_armed()
        mode = mavutil.mode_string_v10(msg)

        if armed and not armed_printed:
            print("Drone armed")
            armed_printed = True

        if not armed and armed_printed:
            print("Drone disarmed")
            break

        if mode == "LOITER" and not loiter_printed:
            print("Mode: LOITER")
            loiter_printed = True

        if mode == "LAND" and not land_printed:
            print("Mode: LAND")
            print("Landing...")
            land_printed = True


    # -------------------------
    # ALTITUDE detection
    # -------------------------
    if msg.get_type() == "GLOBAL_POSITION_INT":

        alt = msg.relative_alt / 1000.0

        if alt > 0.5 and not takeoff_printed:
            print("Takeoff")
            takeoff_printed = True

        if alt >= TARGET_ALT and not target_printed:
            print("Reached target altitude")
            target_printed = True