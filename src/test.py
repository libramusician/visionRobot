import cv2
import numpy as np
from openni import openni2
from openni import _openni2 as c_api

# Initialize the depth device
openni2.initialize(["sdk/libs"])
dev = openni2.Device.open_any()
# Start the depth stream
depth_stream = dev.create_depth_stream()
depth_stream.start()
depth_stream.set_video_mode(c_api.OniVideoMode(
    pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM,
    resolutionX=640, resolutionY=480, fps=30))

while True:
    # Grab a new depth frame
    frame = depth_stream.read_frame()
    frame_data = frame.get_buffer_as_uint16()
    # Put the depth frame into a numpy array and reshape it
    img = np.frombuffer(frame_data, dtype=np.uint16)
    img.shape = (480, 640)

    print(img[240][320])

    # Display the reshaped depth frame using OpenCV
    cv2.imshow("Depth Image", img)
    key = cv2.waitKey(1) & 0xFF
    # If the 'c' key is pressed, break the while loop
    if key == ord("c"):
        break
# Close all windows and unload the depth device
openni2.unload()
cv2.destroyAllWindows()

