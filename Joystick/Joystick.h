#include <fcntl.h>
#include <stdio.h>
#include <linux/joystick.h>

struct axis_state {
    short x, y;
};

class Joystick {
public:
    Joystick(const char* _device);
    ~Joystick();
    int read_event();
    size_t get_axis_count();
    size_t get_button_count();
    size_t get_axis_state();
    size_t get_event_type();
    size_t get_event_number();
    bool get_event_value();
    int get_axis_value_x(size_t axis);
    int get_axis_value_y(size_t axis);

private:
    const char *device;
    int js;
    struct js_event event;
    struct axis_state axes[3];
    size_t axis;
};
