import sys
import os


if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath('..'))
    from command_processor.logitech_gamepad_f710 import LogitechGamepadF710
    from command_processor.logitech_gamepad_f710 import JS_BUTTON_EVENT
    from command_processor.logitech_gamepad_f710 import JS_AXIS_EVENT

    js = LogitechGamepadF710()
    while js.read_event() == 0:
        event_type = js.get_event_type()
        if event_type == JS_BUTTON_EVENT:
            btn_number, btn_state = js.get_button_event()
            print("Button %d %s" % (btn_number, btn_state))
            if btn_number == 0: # button X
                print("Exit")
                break
        elif event_type == JS_AXIS_EVENT:
            axis = js.get_axis_state()
            x, y = js.get_axis_value(axis)
            print("Axis %d (%6d, %6d)" % (axis, x, y))



