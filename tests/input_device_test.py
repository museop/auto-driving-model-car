import sys
import os


if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath('..'))
    from user_input_device.user_input_device import UserEventType
    from user_input_device.logitech_gamepad_f710 import LogitechGamepadF710

    user_input_dev = LogitechGamepadF710()
    print("Device Name: " + user_input_dev.device_name())

    while user_input_dev.is_available():
        user_event, value = user_input_dev.read_user_event()

        if user_event == UserEventType.DEFAULT:
            continue

        print(user_event)
        print([user_event, value])
        if user_event == UserEventType.CHANGE_STEERING_ANGLE:
            print("value: " + str(value))

        elif user_event == UserEventType.EXIT_PROGRAM:
            break


