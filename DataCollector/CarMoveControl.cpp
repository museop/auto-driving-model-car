#include "CarMoveControl.h"
#include <iostream>
using namespace std;

CarMoveControl::CarMoveControl() {
    speedPWM = 0;
    degreePWM = 0;
    pca9685 = new PCA9685();
    pca9685->openPCA9685();
}

CarMoveControl::~CarMoveControl() {
    pca9685->closePCA9685();
    delete pca9685;
}

void CarMoveControl::moveFront(double speed) {
    double pwmDouble;
    pwmDouble = speed;
    this->speedPWM = (int)pwmDouble;
    pca9685->setPWM(MOVE_CHANNEL, 0, this->speedPWM);
}

void CarMoveControl::moveBack(double speed) {
    double pwmDouble;
    pwmDouble = speed;
    this->speedPWM = (int)pwmDouble;
    pca9685->setPWM(MOVE_CHANNEL, 0, NEUTRAL);
    usleep(20000);
    pca9685->setPWM(MOVE_CHANNEL, 0, this->speedPWM);
    usleep(20000);
    pca9685->setPWM(MOVE_CHANNEL, 0, NEUTRAL);
    usleep(20000);
    pca9685->setPWM(MOVE_CHANNEL, 0, this->speedPWM);
    usleep(20000);
}

void CarMoveControl::turnLeft(double degree) {
    double pwmDouble;
    pwmDouble = degree;
    this->degreePWM = (int)pwmDouble;
    pca9685->setPWM(TURN_CHANNEL, 0, this->degreePWM);
}

void CarMoveControl::turnRight(double degree) {
    double pwmDouble;
    pwmDouble = degree;
    this->degreePWM = (int)pwmDouble;
    pca9685->setPWM(TURN_CHANNEL, 0, this->degreePWM);
}

void CarMoveControl::stop() {
    while(this->speedPWM > 307) {
        this->speedPWM--;
        pca9685->setPWM(MOVE_CHANNEL, 0, this->speedPWM);
        usleep(50000);
    }
}

void CarMoveControl::quickBrake() {
    this->speedPWM = 307;
    pca9685->setPWM(MOVE_CHANNEL, 0, this->speedPWM);
}

