from pymavlink import mavutil
import time

TARGET_ALT = 1.0
HOLD_TIME = 5

TAKEOFF_THRUST = 0.65
HOVER_THRUST = 0.5

PORT = "/dev/ttyACM0"
BAUD = 115200

print("Connecting...")
master = mavutil.mavlink_connection(PORT, baud=BAUD)
master.wait_heartbeat()
print("Connected")

# --------------------------------------------------

def set_mode(mode):
    mode_id = master.mode_mapping()[mode]
    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id
    )

def arm():
    master.arducopter_arm()
    master.motors_armed_wait()
    print("Armed")

def disarm():
    master.arducopter_disarm()
    master.motors_disarmed_wait()
    print("Disarmed")

def send_thrust(thrust):
    master.mav.set_attitude_target_send(
        int(time.time()*1e6),
        master.target_system,
        master.target_component,
        0b00000111,   # ignore roll pitch yaw
        [1,0,0,0],
        0,
        0,
        0,
        thrust
    )

def get_altitude():
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    return msg.relative_alt / 1000.0

# --------------------------------------------------
# START
# --------------------------------------------------

set_mode("GUIDED_NOGPS")

arm()

time.sleep(2)

print("Taking off...")

while True:

    alt = get_altitude()
    print(f"Altitude: {alt:.2f}")

    if alt >= TARGET_ALT:
        print("Reached target altitude")
        break

    send_thrust(TAKEOFF_THRUST)
    time.sleep(0.1)

# --------------------------------------------------
# HOVER
# --------------------------------------------------

print("Hovering...")

start = time.time()

while time.time() - start < HOLD_TIME:

    alt = get_altitude()

    if alt < TARGET_ALT - 0.1:
        send_thrust(0.55)

    elif alt > TARGET_ALT + 0.1:
        send_thrust(0.45)

    else:
        send_thrust(HOVER_THRUST)

    time.sleep(0.1)

# --------------------------------------------------
# LAND
# --------------------------------------------------

print("Landing")

set_mode("LAND")

while True:

    alt = get_altitude()
    print(f"Altitude: {alt:.2f}")

    if alt <= 0.15:
        print("Landed")
        break

    time.sleep(0.5)

disarm()