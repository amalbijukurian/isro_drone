from pymavlink import mavutil
import time

TARGET_ALT = 4.0

PORT = "/dev/ttyACM0"
BAUD = 115200

print("Connecting...")
master = mavutil.mavlink_connection(PORT, baud=BAUD)
master.wait_heartbeat()
print("Connected")

armed_printed = False
takeoff_printed = False
target_printed = False
loiter_printed = False
land_printed = False


def get_altitude():
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    return msg.relative_alt / 1000.0


def get_mode():
    msg = master.recv_match(type='HEARTBEAT', blocking=True)
    return mavutil.mode_string_v10(msg)


while True:

    alt = get_altitude()
    mode = get_mode()
    armed = master.motors_armed()

    # ARM
    if armed and not armed_printed:
        print("\nARMED\n")
        armed_printed = True

    # TAKEOFF
    if alt > 0.5 and not takeoff_printed:
        print("Takeoff")
        takeoff_printed = True

    # TARGET ALTITUDE
    if alt >= TARGET_ALT and not target_printed:
        print("Reached target altitude")
        target_printed = True

    # LOITER MODE
    if mode == "LOITER" and not loiter_printed:
        print("Mode: LOITER")
        loiter_printed = True

    # LAND MODE
    if mode == "LAND" and not land_printed:
        print("Mode: LAND")
        print("landing...")
        land_printed = True

    # DISARM
    if not armed and armed_printed:
        print("Drone DISARMED")
        break

    time.sleep(0.5)