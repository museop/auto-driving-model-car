/*
The MIT License (MIT)

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
#include <jetsonGPIO.h>
#include <hgl40dn1Control.h>
#include <ultraSonicSensor.h>

#ifndef HGL40DN1_H_
#define HGL40DN1_H_

class HGL40DN1 : public UltraSonicSensor
{
public:
	HGL40DN1(int uSonicSensorNumber_input, jetsonGPIO triggerGPIO, jetsonGPIO echoGPIO);
	HGL40DN1(int uSonicSensorNumber_input, jetsonGPIO triggerGPIO, jetsonGPIO* echoGPIOList, int echoSensorCount_input);
	~HGL40DN1();

    void sensorOn(void);
    void sensorOff(void);

    double getDistance(int echoSensorN = 0);
    double getTrigulation(void);

private:
    HGL40DN1Control *hgl40dn1Control;

};



#endif // HGL40DN1_H_

