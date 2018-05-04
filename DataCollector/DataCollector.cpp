#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <unistd.h>
#include <thread>
#include <chrono>
#include <ctime>
#include <sys/timeb.h>
#include <string>
#include <opencv2/opencv.hpp>
#include <linux/joystick.h>
#include "CarMove.h"

using namespace std;
using namespace cv;

const double NEUTRAL_VALUE    = 307.0;
const double MOVE_FRONT_SPEED = 328.0;
const double MOVE_BACK_SPEED  = 284.0;
const int MS_INTERVAL         = 30;

bool exited = false;
bool save = false;
short current_angle_pwm = NEUTRAL_VALUE;

void capture_frames()
{
    VideoCapture cap("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)320, height=(int)160,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink");

    struct timeval val;
    struct tm *ptm;
    char dt[30];

    if (!cap.isOpened())
    {
        cout << "cannot open camera..\n";
        return;
    }
    
    FILE *fp = fopen("./data/data.txt", "a");

    while (!exited)
    {
        if (save) {
            gettimeofday(&val, NULL);
            ptm = localtime(&val.tv_sec);

            memset(dt, 0x00, sizeof(dt));

            sprintf(dt, "%04d%02d%02d%02d%02d%02d%06ld.jpg", ptm->tm_year + 1900, ptm->tm_mon = 1, ptm->tm_mday, ptm->tm_hour, ptm->tm_min, ptm->tm_sec, val.tv_usec);

            Mat frame;
            cap >> frame;

            printf("%d\n", current_angle_pwm);

            fprintf(fp, "%s %d\n", dt, current_angle_pwm);

            imwrite(string("./data/") + string(dt), frame);
        }

        this_thread::sleep_for(chrono::milliseconds(MS_INTERVAL)); 
    }

    fclose(fp);

    cap.release();
}

/**
 * Reads a joystick event from the joystick device.
 *
 * Returns 0 on success. Otherwise -1 is returned.
 */
int read_event(int fd, struct js_event *event)
{
    ssize_t bytes;

    bytes = read(fd, event, sizeof(*event));

    if (bytes == sizeof(*event))
        return 0;

    /* Error, could not read full event. */
    return -1;
}

/**
 * Returns the number of axes on the controller or 0 if an error occurs.
 */
size_t get_axis_count(int fd)
{
    __u8 axes;

    if (ioctl(fd, JSIOCGAXES, &axes) == -1)
        return 0;

    return axes;
}

/**
 * Returns the number of buttons on the controller or 0 if an error occurs.
 */
size_t get_button_count(int fd)
{
    __u8 buttons;
    if (ioctl(fd, JSIOCGBUTTONS, &buttons) == -1)
        return 0;

    return buttons;
}

/**
 * Current state of an axis.
 */
struct axis_state {
    short x, y;
};

/**
 * Keeps track of the current axis state.
 *
 * NOTE: This function assumes that axes are numbered starting from 0, and that
 * the X axis is an even number, and the Y axis is an odd number. However, this
 * is usually a safe assumption.
 *
 * Returns the axis that the event indicated.
 */
size_t get_axis_state(struct js_event *event, struct axis_state axes[3])
{
    size_t axis = event->number / 2;

    if (axis < 3) {
        if (event->number % 2 == 0)
            axes[axis].x = event->value;
        else
            axes[axis].y = event->value;
    }

    return axis;
}

short range_map(short x, short in_min, short in_max, short out_min, short out_max)
{
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

int main(int argc, char *argv[])
{
    const char *device;
    int js;
    struct js_event event;
    struct axis_state axes[3] = {0};
    size_t axis;

    if (argc > 1)
        device = argv[1];
    else
        device = "/dev/input/js0";

    js = open(device, O_RDONLY);

    if (js == -1)
        perror("Could not open joystick");

    // Thread for capture frame and steering angle
    thread capturer(&capture_frames);

    // CarMove
    CarMove *carMove = new CarMove();

    /*
     * Button 0: exit
     * Button 1: begin saving data
     * Button 2: end saving data
     * axis 0: move front or back
     * axis 1: steering wheel
     */

    while (read_event(js, &event) == 0)
    {
        switch (event.type)
        {
            case JS_EVENT_BUTTON:
                if (event.number == 0 && event.value)
                {
                    printf("exit..\n");
                    exited = true;
                }
                else if (event.number == 1 && event.value)
                {
                    printf("begin saving..\n");
                    save = true;
                }
                else if (event.number == 2 && event.value)
                {
                    printf("end saving..\n");
                    save = false;
                }

                break;

            case JS_EVENT_AXIS:
                axis = get_axis_state(&event, axes);

                if (axis == 0)
                {
                    if (axes[axis].y < 0)
                    {
                        printf("move front\n");
                        carMove->moveFront(MOVE_FRONT_SPEED);
                    }
                    else if (axes[axis].y > 0)
                    {
                        printf("move back\n");
                        carMove->moveBack(MOVE_BACK_SPEED);
                    }
                    else
                    {
                        printf("stop\n");
                        carMove->moveFront(NEUTRAL_VALUE);
                    }
                }
                else if (axis == 1)
                {
                    current_angle_pwm = range_map(axes[axis].x, -32767, 32767, 235.0, 379.0);
                    
                    if (current_angle_pwm >= NEUTRAL_VALUE)
                    {
                        carMove->turnRight((double)current_angle_pwm);
                    }
                    else
                    {
                        carMove->turnLeft((double)current_angle_pwm);
                    }
                }

                break;

            default:
                /* Ignore init events. */
                break;
        }

        if (exited) break;

    }

    carMove->stop();
    close(js);
    capturer.join();

    return 0;
}
