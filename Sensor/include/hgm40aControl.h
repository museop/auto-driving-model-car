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
#include <pthread.h>
#include <ultraSonicSensorControl.h>

#ifndef HGM40A_CONTROL_H_
#define HGM40A_CONTROL_H_


#define HGM40A_MAX_SENSOR_DISTANCE 	400
#define HGM40A_MAX_SENSOR_DELAY    	2320
#define	HGM40A_SONIC_MAKE_DELAY	   	1450
#define HGM40A_TRIANGULATION_ERROR 	20
#define HGM40A_ECHO_SENSOR_WIDTH	30

class HGM40AControl
{
public:
    HGM40AControl(int uSonicSensorNumber_input, jetsonGPIO triggerGPIO, jetsonGPIO echoGPIO);
    HGM40AControl(int uSonicSensorNumber_input, jetsonGPIO triggerGPIO, jetsonGPIO* echoGPIOList, int echoSensorCount_input) ;
    ~HGM40AControl() ;

static void *Echothread_function(void *arg);
    static void *Triggerthread_function(void *arg);

    void trigSensorInit(void);
    void echoSensorInit(void);

    void trigSensorEnd(void);
    void echoSensorEnd(void);

    void exportGPIO ( void ) ;
    void unexportGPIO ( void ) ;
    void setDirection ( void ) ;

    void removeMSGQ(void);

    double getSensorResult(int echoSensorN) ;		
    double pingMedian (int iterations, int echoSensorN = 0) ;      

    double calculateMedian (int count, double sampleArray[]) ;
    double triangulation_Cal(float dist_leftEllip, float dist_rightEllip, float width);

    void sensorOn(void);
    void sensorOff(void);

    double getDistance(int echoSensorN = 0);
    double getTrigulation(void);
	
    void setUSonicSensorNumber(int sensorNumber);
    int getUSonicSensorNumber(void);

    void setEchoSensorCount(int SensorCount);
    int getEchoSensorCount(void);

    void setMaxSensorDelay(long delayValue);
    long getMaxSensorDelay(void);

    void setSonicMakeDelay(long delayValue);
    long getSonicMakeDelay(void);

	void setEchoSensorWidth(long widthValue);
    long getEchoSensorWidth(void);

    void setMaxSensorDistance(long distanceValue);
    long getMaxSensorDistance(void);

    void setUSonicTrigger(jetsonGPIO uSonicTrigger_);
    jetsonGPIO getUSonicTrigger(void);

    void setUSonicEcho(jetsonGPIO* uSonicEcho_);
    jetsonGPIO getUSonicEcho(int iteratorN);
    
    
private:
    jetsonGPIO uSonicTrigger ;
    list<jetsonGPIO> uSonicEcho_List;

    int uSonicSensorNumber;
    int echoSensorCount;

    long maxSensorDelay;
    long maxSensorDistance;
    long sonicMakeDelay;
	long echoSensorWidth;

    pthread_t p_thread_Trigger;

    uSonicTrigTArg *uSonictArgTrigger;
    uSonicEchoTArg **uSonictArgEcho;				

    pthread_t *P_thread_Echo_Element;

    list<pthread_t> p_thread_Echo_List;
    list<timeval> tval_result;
};



#endif // HGM40ACONTROL_H_

