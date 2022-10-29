import pathlib

import numpy, cv2
import socket

img_id = 1
PATH = pathlib.Path(__file__).parents[1]
IMG_PATH = PATH.joinpath("img")

if __name__ == '__main__':
    ip_robot = "127.0.0.1"
    port = 5500
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (ip_robot, port)
    s.bind(addr)
    print("server up")
    while True:
        try:
            data, address = s.recvfrom(1048576)
            frame_arr = numpy.array(bytearray(data))
            frame = cv2.imdecode(frame_arr, cv2.IMREAD_UNCHANGED)

            cv2.imshow("frame", frame)

        except Exception as e:
            print(e)
            print("connection stopped")
            exit(1)

        if cv2.waitKey(16) == ord('q'):
            break
        elif cv2.waitKey(16) == ord('c'):
            img_name = "tmpImg" + str(img_id) + ".jpg"
            img_path = IMG_PATH.joinpath(img_name)
            print(img_path)
            cv2.imwrite(str(img_path), frame)
            print("image wrote")
            img_id += 1
    cv2.destroyAllWindows()