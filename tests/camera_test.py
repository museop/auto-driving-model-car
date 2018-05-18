import os
import sys


if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath('..'))
    from camera.jetson_tx2_camera import LI_IMX377_MIPI_M12

    camera = LI_IMX377_MIPI_M12()
    camera.show_frames()
