#include "Joystick.h"
#include <unistd.h>
#include <stdlib.h>

Joystick::Joystick(const char* _device)
{
    this->device = _device;
    js = open(device, O_RDONLY);
    if (js == -1) {
        perror("Could not open joystick");
        exit(0);
    }
}

Joystick::~Joystick()
{
    close(js);
}

int Joystick::read_event()
{
    ssize_t bytes;

    bytes = read(js, &event, sizeof(event));

    if (bytes == sizeof(event))
        return 0;

    /* Error, could not read full event. */
    return -1;
}

size_t Joystick::get_axis_count()
{
    __u8 axes;

    if (ioctl(js, JSIOCGAXES, &axes) == -1)
        return 0;

    return axes;
}

size_t Joystick::get_button_count()
{
    __u8 buttons;
    if (ioctl(js, JSIOCGBUTTONS, &buttons) == -1)
        return 0;

    return buttons;
}

size_t Joystick::get_axis_state()
{
    size_t axis = event.number / 2;

    if (axis < 3)
    {
        if (event.number % 2 == 0)
            axes[axis].x = event.value;
        else
            axes[axis].y = event.value;
    }

    return axis;
}

size_t Joystick::get_event_type()
{
    return event.type;
}

size_t Joystick::get_event_number()
{
    return event.number;
}

bool Joystick::get_event_value()
{
    return event.value;
}

int Joystick::get_axis_value_x(size_t axis)
{
    return axes[axis].x;
}

int Joystick::get_axis_value_y(size_t axis)
{
    return axes[axis].y;
}

