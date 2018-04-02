#include <CarSensor.h>

CarSensor::CarSensor() : hgm40a_LGPIO{gpio427, gpio429}, hgm40a_RGPIO{gpio299, gpio410} {
    hgm40a_L = new HGM40A(800, gpio428, hgm40a_LGPIO, 2);
    hgm40a_R = new HGM40A(801, gpio409, hgm40a_RGPIO, 2);
    hgl40dn1 = new HGL40DN1(802, gpio398, gpio388);
    hgm40dn1 = new HGM40DN1(803, gpio392, gpio430);
}

CarSensor::~CarSensor() {
    delete hgm40a_L;
    delete hgm40a_R;
    delete hgl40dn1;
    delete hgm40dn1;
}

void CarSensor::sensorOn() {
    hgm40a_L->sensorOn();
    hgm40a_R->sensorOn();
    hgl40dn1->sensorOn();
    hgm40dn1->sensorOn();
}

void CarSensor::sensorOff() {
    hgm40a_L->sensorOff();
    hgm40a_R->sensorOff();
    hgl40dn1->sensorOff();
    hgm40dn1->sensorOff();
}

int CarSensor::getFrontDistance() {
    int front_distance = hgm40dn1->getDistance();
    return front_distance;
}

int CarSensor::getBackDistance() {
    int back_distance = hgl40dn1->getDistance();
    return back_distance;
}

int CarSensor::getLeftDistance() {
    int side_sensing_diameter = CAR_WIDTH * 3;
    int a_distance_LF = hgm40a_L->getDistance(0) ;
    int a_distance_LB = hgm40a_L->getDistance(1) ;
    
    int side_distance_L = CAR_WIDTH * 3;
    if ((a_distance_LF <= side_sensing_diameter) && (a_distance_LB <= side_sensing_diameter)) {
        side_distance_L = hgm40a_L->getTrigulation();
    }
    else {
        side_distance_L = CAR_WIDTH * 3;
    }
    return side_distance_L;
}

int CarSensor::getRightDistance() {
    int side_sensing_diameter = CAR_WIDTH * 3;
    int a_distance_RF = hgm40a_R->getDistance(0) ;
    int a_distance_RB = hgm40a_R->getDistance(1);
    
    int side_distance_R = CAR_WIDTH * 3;
    if ((a_distance_RF <= side_sensing_diameter) && (a_distance_RB <= side_sensing_diameter)) {
        side_distance_R = hgm40a_R->getTrigulation();
    }
    else {
        side_distance_R = CAR_WIDTH * 3;
    }
    return side_distance_R;
}

