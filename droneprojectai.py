
import cv2
from djitellopy import Tello
import time
from ultralytics import YOLO

# initialize Tello
tello = Tello()
tello.connect()
print(f"Battery: {tello.get_battery()}%")
tello.streamon()  # Start video stream

# Load YOLO model
model = YOLO("best.pt")

counter = 0

# Takeoff
tello.takeoff()
time.sleep(2)
tello.move_up(60)

# Define Zigzag Movement
def zigzag(drone, step=65):
    drone.move_forward(step)
    drone.move_right(step)
    drone.move_forward(step)
    drone.move_left(step)

try:
    while True:
        # Get video frame
        img =  tello.get_frame_read().frame

        # Run YOLO inference
        results = model(img)

        # Annotated frame with detections
        annotated_frame = results[0].plot()

        # Show frames
        cv2.imshow("YOLO-Tello", annotated_frame)

        # Check if any object detected
        if len(results[0].boxes) > 0:
            counter += 1
            print(f"[INFO] Detected something! Counter: {counter}")
            tello.send_rc_control(0, 0, 0, 0)  # stop movement
            time.sleep(15)  # pause 15 sec


        # Move in zigzag
        zigzag(tello, step=65)
        time.sleep(1)

        # Check keys
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    # Safe exit
    tello.land()
    print(f"[INFO] Detected all! Counter: {counter}")
    tello.streamoff()
    tello.end()
    cv2.destroyAllWindows()

except KeyboardInterrupt:
    tello.land()
    tello.streamoff()
    tello.end()
    cv2.destroyAllWindows()
    print("Program interrupted safely.")
