filefrom pymavlink import mavutil
import time

TARGET_ALT = 1.0     # 🔧 meters (EDIT THIS)
HOLD_TIME = 5        # 🔧 seconds (EDIT THIS)

TAKEOFF_THRUST = 0.65
HOVER_THRUST = 0.5
LAND_THRUST = 0.4

PORT = "/dev/ttyACM0"
BAUD = 115200

# ------------------------------------------------------------
# CONNECT
# ------------------------------------------------------------
print("Connecting...")
master = mavutil.mavlink_connection(PORT, baud=BAUD)
master.wait_heartbeat()
print("Connected")

# --------------------------------------------------
# HELPERS
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

def loiter(duration):
    set_mode("LOITER")
    print("Loitering...")
    time.sleep(duration)

def land():
    set_mode("LAND")
    print("Landed")

def send_thrust(thrust):
    master.mav.set_attitude_target_send(
        0,
        master.target_system,
        master.target_component,
        0,
        [1, 0, 0, 0],
        0, 0, 0,
        thrust
    )

def get_altitude():
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    return msg.relative_alt / 1000.0  # meters

# --------------------------------------------------
# MAIN LOGIC
# --------------------------------------------------

set_mode("GUIDED_NOGPS")
arm()

time.sleep(2)

print("Taking off...")

# --- TAKEOFF LOOP ---
while True:
    alt = get_altitude()
    print(f"Altitude: {alt:.2f} m")

    if alt >= TARGET_ALT:
        print("Reached target altitude")
        break

    send_thrust(TAKEOFF_THRUST)

"""# --- HOLD ---
print("Holding...")
start = time.time()

while time.time() - start < HOLD_TIME:
    alt = get_altitude()

    # simple stabilization
    if alt < TARGET_ALT - 0.1:
        send_thrust(0.55)
    elif alt > TARGET_ALT + 0.1:
        send_thrust(0.45)
    else:
        send_thrust(HOVER_THRUST)"""

# --- LAND ---

print("loiter")
loiter(10)
print("Landing...")
land()

"""while True:
    alt = get_altitude()
    print(f"Altitude: {alt:.2f} m")

    if alt <= 0.15:
        print("Landed")
        send_thrust(0)
        break

    send_thrust(LAND_THRUST)"""
