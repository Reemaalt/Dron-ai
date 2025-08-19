import cv2
import time
from djitellopy import Tello

# Initialize 
tello = Tello()
tello.connect()
print(f"Battery: {tello.get_battery()}%")

# Start video stream
tello.streamon()
frame_read = tello.get_frame_read()

# Takeoff
tello.takeoff()
time.sleep(2)

# Fly in a triangle path with live video
for i in range(3):  
    tello.move_forward(100)        
    tello.rotate_clockwise(120)    # turn 120° (triangle corner)
    time.sleep(1)

    # Show video while flying
    for _ in range(50):  # display ~50 frames between moves
        frame = frame_read.frame
        cv2.imshow("Tello Stream", frame)
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            tello.land()
            tello.streamoff()
            tello.end()
            cv2.destroyAllWindows()
            exit()

# Capture the last frame after triangle flight
frame = frame_read.frame
cv2.imwrite("triangle_original.jpg", frame)

# Land
tello.land()
# Stop stream
tello.streamoff()
tello.end()
cv2.destroyAllWindows()
