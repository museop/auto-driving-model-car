#include "Joystick.h"

extern "C"
{
    Joystick* new_joystick(const char* device) {
        return new Joystick(device);
    }
    
    int read_event(Joystick* joy) {
        return joy->read_event();
    }

    int get_axis_count(Joystick* joy) {
        return joy->get_axis_count();
    }

    int get_button_count(Joystick* joy) {
        return joy->get_button_count();
    }

    int get_axis_state(Joystick* joy) {
        return joy->get_axis_state();
    }

    int get_event_type(Joystick* joy) {
        return joy->get_event_type();
    }

    int get_event_number(Joystick* joy) {
        return joy->get_event_number();
    }

    int get_event_value(Joystick* joy) {
        return joy->get_event_value();
    }

    int get_axis_value_x(Joystick* joy, int axis) {
        return joy->get_axis_value_x(axis);
    }

    int get_axis_value_y(Joystick* joy, int axis) {
        return joy->get_axis_value_y(axis);
    }
}
