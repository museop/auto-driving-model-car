#ifndef __CARMOVECONTROL_H__
#define __CARMOVECONTROL_H__

#define TURN_CHANNEL 0
#define MOVE_CHANNEL 1
#define NEUTRAL 307

#include <unistd.h>
#include "JHPWMPCA9685.h"

class CarMoveControl {
private:
    int speedPWM;
    int degreePWM;
    PCA9685 *pca9685;

public:
    CarMoveControl();
    ~CarMoveControl();

    void moveFront(double speed);
    void moveBack(double speed);
    void turnLeft(double degree);
    void turnRight(double degree);
    void stop();
    void quickBrake();
};

#endif

