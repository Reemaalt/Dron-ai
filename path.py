import cv2
from djitellopy import Tello
import time

# --------------------------
# 1. Initialize Tello
# --------------------------
tello = Tello()
tello.connect()
print(f"Battery: {tello.get_battery()}%")
tello.streamon()  # Start video stream
frame_read = tello.get_frame_read()

# Takeoff
tello.takeoff()
time.sleep(2)

# --------------------------
# 2. Define Zigzag Movement
# --------------------------
def zigzag(drone, step=30):
    """
    Moves forward-right-forward-left (zigzag).
    step = distance in cm (must be between 20–500).
    """
    drone.move_forward(step)
    drone.move_right(step)
    drone.move_forward(step)
    drone.move_left(step)

# --------------------------
# 3. Placeholder for model (fake detection)
# --------------------------
def placeholder_model(frame):
    """
    Placeholder for your ML model.
    For now it just returns False (no detection).
    Replace with your real model later.
    """
    return False

# --------------------------
# 4. Main Loop
# --------------------------
try:
    while True:
        # Get video frame
        img = frame_read.frame
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Show frames
        cv2.imshow("Tello Original Frame", img)
        cv2.imshow("Tello Grayscale Frame", gray_img)

        # Check keys
        key = cv2.waitKey(1) & 0xFF

        # If 'd' pressed → pause drone
        if key == ord('d'):
            print("🔴 Detection simulated → Drone pausing for 5 seconds...")
            tello.send_rc_control(0, 0, 0, 0)  # stop any motion
            time.sleep(5)

        # Quit program
        if key == ord('q'):
            break

        # Run placeholder model (can later replace with YOLO/CNN detection)
        detected = placeholder_model(img)
        if detected:
            print("Model detected object → Pausing 5s...")
            tello.send_rc_control(0, 0, 0, 0)
            time.sleep(5)

        # Move in zigzag
        zigzag(tello, step=30)
        time.sleep(1)

    # Safe exit
    tello.land()
    tello.streamoff()
    tello.end()
    cv2.destroyAllWindows()

except KeyboardInterrupt:
    tello.land()
    tello.streamoff()
    tello.end()
    cv2.destroyAllWindows()
    print("Program interrupted safely.")
