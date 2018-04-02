#ifndef __CAR_SENSOR_H__
#define __CAR_SENSOR_H__

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>
#include <time.h>
#include <sys/time.h>
#include <iostream>
#include <unistd.h>
#include <jetsonGPIO.h>
#include <hgm40a.h>
#include <hgl40dn1.h>
#include <hgm40dn1.h>


#define CAR_WIDTH  30
#define CAR_HEIGHT 40

class CarSensor {
public:
    CarSensor();
    ~CarSensor();
    void sensorOn();
    void sensorOff();
    int getFrontDistance();
    int getBackDistance();
    int getLeftDistance();
    int getRightDistance();

private:
    HGM40A *hgm40a_L;
    HGM40A *hgm40a_R;
    
    HGL40DN1 *hgl40dn1;
    HGM40DN1 *hgm40dn1;

    jetsonGPIO hgm40a_LGPIO[2];
    jetsonGPIO hgm40a_RGPIO[2];
};

#endif
