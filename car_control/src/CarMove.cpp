#include "CarMove.h"
#include <iostream>
using namespace std;

CarMove::CarMove() {
    speed = 0;
    degree = 0;
}

CarMove::~CarMove() {
}

void CarMove::setSpeed(double speed) {
    this->speed = speed;
}

void CarMove::setDegree(double degree) {
    this->degree = degree;
}

double CarMove::getSpeed() {
    return this->speed;
}

double CarMove::getDegree() {
    return this->degree;
}

void CarMove::moveFront(double speed) {
    if (speed >= MAXSPEED) {
        speed = MAXSPEED;
    }
    else if (speed < 307) {
        speed = 307;
    }

    setSpeed(speed);
    carMoveControl.moveFront(speed);
}

void CarMove::moveBack(double speed) {
    if (speed >= MAXSPEED) {
        speed = MAXSPEED;
    }
    else if (speed > 307) {
        speed = 307;
    }

    setSpeed(speed);
    carMoveControl.moveBack(speed);
}

void CarMove::turnLeft(double degree) {
    if (degree >= MAXDEGREE) {
        degree = MAXDEGREE;
    }
    else if (degree > 307) {
        degree = 307;
    }

    setDegree(degree);
    carMoveControl.turnLeft(degree);
}

void CarMove::turnRight(double degree) {
    if (degree >= MAXDEGREE) {
        degree = MAXDEGREE;
    }
    else if (degree < 307) {
        degree = 307;
    }

    setDegree(degree);
    carMoveControl.turnRight(degree);
}

void CarMove::stop() {
    carMoveControl.stop();
    setSpeed(307);
}

void CarMove::quickBrake() {
    carMoveControl.quickBrake();
    setSpeed(307);
}

