import os
import sys


if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath('..'))
    from camera.jetson_tx2_camera import JetsonTX2Camera

    camera = JetsonTX2Camera()
    camera.show_frames()
