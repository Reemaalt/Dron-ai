import cv2
from djitellopy import Tello
import time

# initialize Tello
tello = Tello()
tello.connect()
print(f"Battery: {tello.get_battery()}%")
tello.streamon()  # Start video stream
frame_read = tello.get_frame_read()
'''
model = YOLO()

'''
counter = 0

# Takeoff
tello.takeoff()
time.sleep(2)
tello.move_up(50)

# Define Zigzag Movement
def zigzag(drone, step=50):

    drone.move_forward(step)
    drone.move_right(step)
    drone.move_forward(step)
    drone.move_left(step)


try:
    while True:
        # Get video frame
        img = frame_read.frame
        # results = model (img)
        # Show frames // change to show model frame so we see real time :)
        cv2.imshow("Tello Original Frame", img)

        # Check keys
        key = cv2.waitKey(1) & 0xFF

        # Draw detections
        """
        annotated_frame = results[0].plot()
        cv2.imshow("YOLO-Tello", annotated_frame)

        # Check if any object detected
        if len(results[0].boxes) > 0:
            counter += 1
            print(f"[INFO] Detected something! Counter: {counter}")
            tello.send_rc_control(0, 0, 0, 0)  # stop movement
            time.sleep(15)  # pause 15 sec
        """
        # Quit program
        if key == ord('q'):
            break

        # Run placeholder model


        # Move in zigzag
        zigzag(tello, step=50)
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