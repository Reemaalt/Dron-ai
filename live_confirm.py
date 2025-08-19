import cv2
import time
from djitellopy import Tello

# Initialize Tello
tello = Tello()
tello.connect()
print(f"Battery: {tello.get_battery()}%")

# Start video stream
tello.streamon()
frame_read = tello.get_frame_read()

# Takeoff
tello.takeoff()
time.sleep(2)

confirmed = False

while True:

    frame = frame_read.frame
    cv2.imshow("Tello Stream", frame)

    # Move forward slowly
    tello.move_forward(20)   
    time.sleep(2)            # wait ccc

    # Check for confirmation key
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):   # Press 'c' to confirm
        confirmed = True
        cv2.imwrite("confirm_original.jpg", frame)
        tello.flip_left()	
        # Land
        break
    elif key == ord('q'): # Press 'q' to quit without confirm
         # Land
        break


# Land
tello.land()

# Stop stream
tello.streamoff()
tello.end()
cv2.destroyAllWindows()
