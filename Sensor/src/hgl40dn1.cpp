/*
 * The MIT License (MIT)

Copyright (c) 2015 Jetsonhacks

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include "hgl40dn1.h"
#include <iostream>

HGL40DN1::HGL40DN1(int uSonicSensorNumber_input, jetsonGPIO triggerGPIO, jetsonGPIO echoGPIO){
	hgl40dn1Control = new HGL40DN1Control(uSonicSensorNumber_input, triggerGPIO, echoGPIO);
}

HGL40DN1::HGL40DN1(int uSonicSensorNumber_input, jetsonGPIO triggerGPIO, jetsonGPIO* echoGPIOList, int echoSensorCount_input){
	hgl40dn1Control = new HGL40DN1Control(uSonicSensorNumber_input, triggerGPIO, echoGPIOList, echoSensorCount_input);
}

HGL40DN1::~HGL40DN1(){};

void HGL40DN1::sensorOn(void){
	hgl40dn1Control->sensorOn();
}

void HGL40DN1::sensorOff(void){
	hgl40dn1Control->sensorOff();
}

double HGL40DN1::getDistance(int echoSensorN){
	return hgl40dn1Control->getDistance(echoSensorN);
}

double HGL40DN1::getTrigulation(void){
	return hgl40dn1Control->getTrigulation();
}

