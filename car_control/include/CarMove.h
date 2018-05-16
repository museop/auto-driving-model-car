#ifndef __CARMOVE_H__
#define __CARMOVE_H__

#define MAXSPEED 340
#define MAXDEGREE 380

#include "CarMoveControl.h"

class CarMove {
private:
    double speed;
    double degree;
    CarMoveControl carMoveControl;

public:
    CarMove();
    ~CarMove();

    void setSpeed(double speed);
    void setDegree(double degree);
    double getSpeed();
    double getDegree();

    void moveFront(double speed);
    void moveBack(double speed);
    void turnLeft(double degree);
    void turnRight(double degree);
    void stop();
    void quickBrake();
};

#endif

