#include "CarMove.h"

extern "C"
{
    CarMove* CarMove_new() {
        return new CarMove();
    }

    void CarMove_setSpeed(CarMove* c, double speed) {
        c->setSpeed(speed);
    }

    void CarMove_setDegree(CarMove* c, double degree) {
        c->setDegree(degree);
    }

    double CarMove_getSpeed(CarMove* c) {
        return c->getSpeed();
    }

    double CarMove_getDegree(CarMove* c) {
        return c->getDegree();
    }

    void CarMove_moveFront(CarMove* c, double speed) {
        c->moveFront(speed);
    }

    void CarMove_moveBack(CarMove* c, double speed) {
        c->moveBack(speed);
    }

    void CarMove_turnLeft(CarMove* c, double degree) {
        c->turnLeft(degree);
    }

    void CarMove_turnRight(CarMove* c, double degree) {
        c->turnRight(degree);
    }

    void CarMove_stop(CarMove* c) {
        c->stop();
    }

    void CarMove_quickBrake(CarMove* c) {
        c->quickBrake();
    }
}
