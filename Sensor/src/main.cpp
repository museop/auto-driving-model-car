#include <iostream>
#include <termios.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>
#include <CarSensor.h>

using namespace std;

int getkey() {
    int character;
    struct termios orig_term_attr;
    struct termios new_term_attr;

    /* set the terminal to raw mode */
    tcgetattr(fileno(stdin), &orig_term_attr);
    memcpy(&new_term_attr, &orig_term_attr, sizeof(struct termios));
    new_term_attr.c_lflag &= ~(ECHO|ICANON);
    new_term_attr.c_cc[VTIME] = 0;
    new_term_attr.c_cc[VMIN] = 0;
    tcsetattr(fileno(stdin), TCSANOW, &new_term_attr);

    /* read a character from the stdin stream without blocking */
    /*   returns EOF (-1) if no character is available */
    character = fgetc(stdin);

    /* restore the original terminal attributes */
    tcsetattr(fileno(stdin), TCSANOW, &orig_term_attr);

    return character;
}

int main() {
    CarSensor* carSensor = new CarSensor();
    carSensor->sensorOn();
    while (getkey() != 27) {
        int front_dist = carSensor->getFrontDistance();
        int back_dist = carSensor->getBackDistance();
        int left_dist = carSensor->getLeftDistance();
        int right_dist = carSensor->getRightDistance();
        cout << "front dist: " << front_dist << " ";
        cout << "back dist: " << back_dist << " ";
        cout << "left dist: " << left_dist << " ";
        cout << "right dist: " << right_dist << '\n';
        usleep(100000);
    }
    carSensor->sensorOff();
    delete carSensor;
    return 0;
}
