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
#include <math.h>
#include "hgl40dn1Control.h"
#include <iostream>

using namespace std;

HGL40DN1Control::HGL40DN1Control(int uSonicSensorNumber_input, jetsonGPIO triggerGPIO, jetsonGPIO echoGPIO){
    jetsonGPIO echoGPIOList[] = {echoGPIO};

    setEchoSensorCount(1);
    setUSonicTrigger(triggerGPIO);
    setUSonicEcho(echoGPIOList);
    setUSonicSensorNumber(uSonicSensorNumber_input);
    setMaxSensorDistance(HGL40DN1_MAX_SENSOR_DISTANCE);
    setMaxSensorDelay(HGL40DN1_MAX_SENSOR_DELAY);
    setSonicMakeDelay(HGL40DN1_SONIC_MAKE_DELAY);
}

HGL40DN1Control::HGL40DN1Control(int uSonicSensorNumber_input, jetsonGPIO triggerGPIO, jetsonGPIO* echoGPIOList, int echoSensorCount_input){

    setEchoSensorCount(echoSensorCount_input);
    setUSonicTrigger(triggerGPIO);
    setUSonicEcho(echoGPIOList);
    setUSonicSensorNumber(uSonicSensorNumber_input);
	setEchoSensorWidth(HGL40DN1_ECHO_SENSOR_WIDTH);
    setMaxSensorDistance(HGL40DN1_MAX_SENSOR_DISTANCE);
    setMaxSensorDelay(HGL40DN1_MAX_SENSOR_DELAY);
    setSonicMakeDelay(HGL40DN1_SONIC_MAKE_DELAY);
}

HGL40DN1Control::~HGL40DN1Control() {
}


void HGL40DN1Control::removeMSGQ(void){
    key_t sensorQid;

    sensorQid = msgget( (key_t)getUSonicSensorNumber(), IPC_CREAT|0666);
	
    msgctl(sensorQid,IPC_RMID,0);
}


void HGL40DN1Control::trigSensorInit(void){

    uSonictArgTrigger = (uSonicTrigTArg *)malloc(sizeof(uSonicTrigTArg));
    uSonictArgTrigger->sensorGPIO = getUSonicTrigger();
    uSonictArgTrigger->sensorNumber = getUSonicSensorNumber();
    uSonictArgTrigger->uSonicEchoSensorCount = getEchoSensorCount();
    pthread_create(&p_thread_Trigger, NULL, &Triggerthread_function, (void*)uSonictArgTrigger);
}

void HGL40DN1Control::echoSensorInit(void){

    int echoSensorCount = getEchoSensorCount();

    uSonictArgEcho = (uSonicEchoTArg **)malloc(echoSensorCount);
    P_thread_Echo_Element = (pthread_t *)malloc(sizeof(pthread_t) * echoSensorCount);

    for(int i = 0; i < echoSensorCount; i++){

	uSonictArgEcho[i] = (uSonicEchoTArg *)malloc(sizeof(uSonicEchoTArg));
   	uSonictArgEcho[i]->sensorGPIO = getUSonicEcho(i);
    	uSonictArgEcho[i]->sensorNumber = getUSonicSensorNumber();
	uSonictArgEcho[i]->uSonicEchoSensorN = i;
    	uSonictArgEcho[i]->maxSensorDelay = getMaxSensorDelay();
    	uSonictArgEcho[i]->maxSensorDistance = getMaxSensorDistance();
   	uSonictArgEcho[i]->sonicMakeDelay = getSonicMakeDelay();

	pthread_create(&P_thread_Echo_Element[i], NULL, &Echothread_function, (void*)uSonictArgEcho[i]);
	p_thread_Echo_List.push_back(P_thread_Echo_Element[i]);
    }
}

void HGL40DN1Control::trigSensorEnd(void) {
    key_t sensorQid;
    
    uSonicEndMsg endMsg_t = {TRIG_END_MSG_TYPE,SENSOR_END};
    
    sensorQid = msgget( (key_t)getUSonicSensorNumber(), IPC_CREAT|0666);
    
    if(msgsnd(sensorQid,&endMsg_t,sizeof(endMsg_t),IPC_NOWAIT) == -1){
		perror("//Trigger End Msg Send Error // ");
    }
    
    pthread_join(p_thread_Trigger, NULL);
}

void HGL40DN1Control::echoSensorEnd(void) {
    key_t sensorQid;

    uSonicEndMsg endMsg_e = {ECHO_END_MSG_TYPE,SENSOR_END};
	
    sensorQid = msgget( (key_t)getUSonicSensorNumber(), IPC_CREAT|0666);

    list<pthread_t>::iterator pthread_echo_iter = p_thread_Echo_List.begin();
    for(int i = 0; i < getEchoSensorCount(); i++)
    {
	endMsg_e = {ECHO_END_MSG_TYPE + MSG_CODE_INTERVAL * i,SENSOR_END};

    	if(msgsnd(sensorQid,&endMsg_e,sizeof(endMsg_e),IPC_NOWAIT) == -1){
		perror("//Echo End Msg Send Error // ");
   	}

    	pthread_join(*pthread_echo_iter, NULL);
	pthread_echo_iter++;
    }
}

void HGL40DN1Control::exportGPIO ( void ) {
   
    jetsonGPIO uSonicTriggerGPIO,uSonicEchoGPIO;
    
    uSonicTriggerGPIO = getUSonicTrigger();

    gpioExport(uSonicTriggerGPIO) ;

    for(int i = 0; i < getEchoSensorCount(); i++)
    {
	uSonicEchoGPIO = getUSonicEcho(i);
 	gpioExport(uSonicEchoGPIO) ;	
    }
}

void HGL40DN1Control::unexportGPIO ( void ) {

    jetsonGPIO uSonicTriggerGPIO,uSonicEchoGPIO;
    
    uSonicTriggerGPIO = getUSonicTrigger();

    gpioUnexport(uSonicTriggerGPIO) ;

    for(int i = 0; i < getEchoSensorCount(); i++)
    {
	uSonicEchoGPIO = getUSonicEcho(i);
 	gpioUnexport(uSonicEchoGPIO) ;	
    }
}

void HGL40DN1Control::setDirection ( void ) {

    jetsonGPIO uSonicTriggerGPIO,uSonicEchoGPIO;
    
    uSonicTriggerGPIO = getUSonicTrigger();

    gpioSetDirection(uSonicTriggerGPIO,outputPin) ;

    for(int i = 0; i < getEchoSensorCount(); i++)
    {
	uSonicEchoGPIO = getUSonicEcho(i);
 	gpioSetDirection(uSonicEchoGPIO,inputPin);	
    }
}

void HGL40DN1Control::sensorOn(void){
    exportGPIO();
    setDirection();
    trigSensorInit();
    echoSensorInit();
}

void HGL40DN1Control::sensorOff(void){
    free(uSonictArgTrigger);
    free(P_thread_Echo_Element);
    free(uSonictArgEcho);

    cout<<"stop start \n";
    trigSensorEnd();
    echoSensorEnd();
    cout<<"unexport start  \n";
    unexportGPIO();
    removeMSGQ();
}

void HGL40DN1Control::setUSonicSensorNumber(int sensorNumber){
    uSonicSensorNumber = sensorNumber;
}
int HGL40DN1Control::getUSonicSensorNumber(void){
    return uSonicSensorNumber;	
}

void HGL40DN1Control::setEchoSensorCount(int SensorCount){
    echoSensorCount = SensorCount;
}

int HGL40DN1Control::getEchoSensorCount(void){
    return echoSensorCount;
}


void HGL40DN1Control::setMaxSensorDelay(long delayValue){
    maxSensorDelay = delayValue;
}
long HGL40DN1Control::getMaxSensorDelay(void){
    return maxSensorDelay;	
}

void HGL40DN1Control::setSonicMakeDelay(long delayValue){
    sonicMakeDelay = delayValue;
}
long HGL40DN1Control::getSonicMakeDelay(void){
    return sonicMakeDelay;	
}

void HGL40DN1Control::setEchoSensorWidth(long widthValue){
	echoSensorWidth = widthValue;
}
long HGL40DN1Control::getEchoSensorWidth(void){
	return echoSensorWidth;
}

void HGL40DN1Control::setMaxSensorDistance(long distanceValue){
    maxSensorDistance = distanceValue;
}
long HGL40DN1Control::getMaxSensorDistance(void){
    return maxSensorDistance;
}

void HGL40DN1Control::setUSonicTrigger(jetsonGPIO uSonicTrigger_){
    uSonicTrigger = uSonicTrigger_; 
}
jetsonGPIO HGL40DN1Control::getUSonicTrigger(void){
    return uSonicTrigger;
}

void HGL40DN1Control::setUSonicEcho(jetsonGPIO* uSonicEchoGPIO_){
    jetsonGPIO uSonicEcho;
    int echoSensorCount = getEchoSensorCount();
    for(int i = 0; i < echoSensorCount; i++)
    {
    	uSonicEcho = uSonicEchoGPIO_[i];
    	uSonicEcho_List.push_back(uSonicEcho);
    }
}
jetsonGPIO HGL40DN1Control::getUSonicEcho(int iteratorN){

    list<jetsonGPIO>::iterator uSonicEchoGPIO_iter = uSonicEcho_List.begin();
    for(int i = 0; i < iteratorN; i++)
    {
	uSonicEchoGPIO_iter++;
    }
    return *uSonicEchoGPIO_iter;
}


double HGL40DN1Control::getSensorResult (int echoSensorN) {
    int tval_result_usec  = 0, msg_code_interval, msglen;

    uSonicTvalMsg resultTvalMsg;
    timeval tval_result_pre;

    msg_code_interval = MSG_CODE_INTERVAL * echoSensorN;

    list<timeval>::iterator tval_iter = tval_result.begin();
    for(int i = 0; i < echoSensorN; i ++)
    {
	tval_iter++;
    }

    key_t sensorQid = msgget((key_t)getUSonicSensorNumber(), IPC_CREAT|0666);
		
    msglen = msgrcv(sensorQid, &resultTvalMsg, sizeof(resultTvalMsg), RESULT_MSG_TYPE + msg_code_interval, IPC_NOWAIT);
    if(msglen != -1){
	tval_result_pre = *tval_iter;
        *tval_iter = resultTvalMsg.timeval_data;	
    }
    tval_result_usec = tval_iter->tv_sec*1000000+tval_iter->tv_usec-getSonicMakeDelay();
    if(tval_result_usec < 0){
	*tval_iter = tval_result_pre;
	tval_result_usec = tval_iter->tv_sec*1000000+tval_iter->tv_usec-getSonicMakeDelay();
    }
    return tval_result_usec;
}

void * HGL40DN1Control::Echothread_function(void *arg){
    jetsonGPIO uSonicEcho;
	
    int thread_end = 0, msglen;
    int uSonicSensorNumber;
    int echoSensorNumber;
    int maxSensorDelay;
    int maxSensorDistance;

    int msg_code_interval; 

    int sonicMakeDelay;

    uSonicEchoTArg *echoThreadArg = (uSonicEchoTArg *)arg;
	
    uSonicEcho = echoThreadArg->sensorGPIO;
    uSonicSensorNumber = echoThreadArg->sensorNumber;
    echoSensorNumber = echoThreadArg->uSonicEchoSensorN;
    maxSensorDelay = echoThreadArg->maxSensorDelay;
    maxSensorDistance = echoThreadArg->maxSensorDistance;

    sonicMakeDelay = echoThreadArg->sonicMakeDelay;

    msg_code_interval = MSG_CODE_INTERVAL * echoSensorNumber;

    timeval tval_result, tval_before, tval_after;
	
    uSonicTvalMsg trigTvalMsg;
    uSonicEndMsg echoEndMsg;
	
    key_t sensorQid = msgget((key_t)uSonicSensorNumber, IPC_CREAT|0666);
	
    bool isMaxEchoOver = false;
    unsigned int echoValue = low ;
    unsigned int maxEcho = maxSensorDistance*ROUNDTRIP_CM + maxSensorDelay + sonicMakeDelay;
    while(thread_end != SENSOR_END){

        msglen = msgrcv(sensorQid, &trigTvalMsg, sizeof(trigTvalMsg), TRIG_MSG_TYPE + msg_code_interval,IPC_NOWAIT);
        if(msglen != -1){
            tval_before = trigTvalMsg.timeval_data;
            gpioGetValue(uSonicEcho,&echoValue) ;
            isMaxEchoOver = false;

            while (echoValue != high) {
		gpioGetValue(uSonicEcho,&echoValue) ;
	
		gettimeofday(&tval_after, NULL);
		timersub(&tval_after, &tval_before, &tval_result);
		if (echoValue==high) {
		    break;
		}
		if (tval_result.tv_sec*1000000+tval_result.tv_usec > maxEcho) {
                    isMaxEchoOver = true;
                    break;
		}
		}

                uSonicTvalMsg echoTvalMsg = {RESULT_MSG_TYPE + msg_code_interval,tval_result};
                if(msgsnd(sensorQid,&echoTvalMsg,sizeof(echoTvalMsg),IPC_NOWAIT) == -1){
                    perror("//Result TimeVal Send Error//;");
		}

        	usleep(10);
            uSonicTrigMsg tirgMsg = {ECHO_MSG_TYPE + msg_code_interval,READY};
            if(msgsnd(sensorQid,&tirgMsg,sizeof(tirgMsg),IPC_NOWAIT) == -1){
                perror("//Trigger Start Msg Send Error//;");
            }

	}
        msglen = msgrcv(sensorQid, &echoEndMsg, sizeof(echoEndMsg), ECHO_END_MSG_TYPE + msg_code_interval, IPC_NOWAIT);
        if(msglen != -1){
            thread_end = echoEndMsg.msg_end;
        }
        echoValue = low;
    }
}
void * HGL40DN1Control::Triggerthread_function(void *arg){
    jetsonGPIO UltraSonicSensorTrigger;
	
    int thread_end = 0, msglen, uSonicSensorNumber, echoSensorCount, msg_code_interval, i;

    uSonicTrigTArg *trigThreadArg = (uSonicTrigTArg *)arg;

    UltraSonicSensorTrigger = trigThreadArg->sensorGPIO;
    uSonicSensorNumber = trigThreadArg->sensorNumber;
    echoSensorCount = trigThreadArg->uSonicEchoSensorCount;

    cout<<UltraSonicSensorTrigger<<"   "<<uSonicSensorNumber<< "   "<<echoSensorCount<<"  \n";
    int trig_start = echoSensorCount;

    msg_code_interval = MSG_CODE_INTERVAL;
	
    timeval tval_before;

    key_t sensorQid = msgget((key_t)uSonicSensorNumber, IPC_CREAT|0666);

    uSonicEndMsg trigEndMsg;

    uSonicTrigMsg trigReadyMsg;

    uSonicTvalMsg trigTvalMsg;
	
    while(thread_end != SENSOR_END){

        if(trig_start == echoSensorCount){
            gettimeofday(&tval_before, NULL);
	    for(i = 0; i < echoSensorCount; i++){
	
		msg_code_interval = MSG_CODE_INTERVAL * i;
            	trigTvalMsg = {TRIG_MSG_TYPE + msg_code_interval,tval_before};
            	if(msgsnd(sensorQid,&trigTvalMsg,sizeof(trigTvalMsg),IPC_NOWAIT) == -1){
                    perror("//Trigger TimeVal Send Error//");
            	}
	    }
            gpioSetValue(UltraSonicSensorTrigger,low) ;
            for(int i=0; i<40; i++){
                usleep(12.5) ;
                gpioSetValue(UltraSonicSensorTrigger,high) ;
                usleep(12.5) ;
                gpioSetValue(UltraSonicSensorTrigger,low) ;
            }
            usleep(60000) ;
            trig_start = 0;
        }
        msglen = msgrcv(sensorQid, &trigEndMsg, sizeof(trigEndMsg), TRIG_END_MSG_TYPE, IPC_NOWAIT);
        if(msglen != -1){
            thread_end = trigEndMsg.msg_end;
        }

	for(i = 0; i < echoSensorCount; i++){
	    msg_code_interval = MSG_CODE_INTERVAL * i;
            msglen = msgrcv(sensorQid, &trigReadyMsg, sizeof(trigReadyMsg), ECHO_MSG_TYPE + msg_code_interval, IPC_NOWAIT);
       	    if(msglen != -1){
            	trig_start += trigReadyMsg.trig_ready;
            }
	}
    }
}


double HGL40DN1Control::calculateMedian (int count, double sampleArray[]) {
    double tempValue ;
    int i,j ; 
    for (i=0 ; i < count-1; i++) {
        for (j=0; j<count; j++) {
            if (sampleArray[j] < sampleArray[i]) {

                tempValue = sampleArray[i] ;
                sampleArray[i] = sampleArray[j] ;
                sampleArray[j] = tempValue ;
            }
        }
    }

    if (count%2==0) {
        
        return ((sampleArray[count/2] + sampleArray[count/2-1]) / 2.0) ;
    } else {

        return (sampleArray[count/2]) ;
    }
}


double HGL40DN1Control::pingMedian (int iterations, int echoSensorN) {
    double pings[iterations] ;
    double lastPing ;
    int index = 0 ;
    int samples = iterations ;
    int cursor = 0 ;
    pings[0] = NO_ECHO ;
    while (index < iterations) {
        lastPing = getSensorResult(echoSensorN) ;
        if (lastPing != NO_ECHO) {
           
            pings[cursor] = lastPing ;
            cursor ++ ;
        } else {
        
            samples -- ;
        }
        index ++ ;
        usleep(10) ; 
    }

    if (samples == 0) return NO_ECHO ;
    return calculateMedian(samples,pings) ;
}

double HGL40DN1Control::triangulation_Cal(float dist_leftEllip, float dist_rightEllip, float width)
{
    float x_plus  = 0.0, x_minus = 0.0, y, x_answer;
    float ellipseLeft_a = dist_leftEllip;
    float ellipseRight_a = dist_rightEllip;
	float width_x = width / 2.0;
    if(ellipseLeft_a == ellipseRight_a){
        x_answer = 0;
    }
    else{
        x_plus = ((-(4 * (ellipseRight_a * ellipseRight_a)*(ellipseLeft_a * ellipseLeft_a) - 2 * (ellipseRight_a * ellipseRight_a)*(width_x * width_x) - 2 * (ellipseLeft_a * ellipseLeft_a)*(width_x * width_x)) + (2 * (ellipseRight_a)*(ellipseLeft_a)*sqrt(((ellipseRight_a * ellipseRight_a) + (ellipseLeft_a * ellipseLeft_a)) * ((ellipseRight_a * ellipseRight_a) + (ellipseLeft_a * ellipseLeft_a)) - 4 * (width_x * width_x)
            * ((ellipseRight_a * ellipseRight_a) + (ellipseLeft_a * ellipseLeft_a) - (width_x * width_x))))) / (2 * width_x*((ellipseLeft_a * ellipseLeft_a) - (ellipseRight_a * ellipseRight_a))));
        x_minus = ((-(4 * (ellipseRight_a * ellipseRight_a)*(ellipseLeft_a * ellipseLeft_a) - 2 * (ellipseRight_a * ellipseRight_a)*(width_x * width_x) - 2 * (ellipseLeft_a * ellipseLeft_a)*(width_x * width_x)) - (2 * (ellipseRight_a)*(ellipseLeft_a)*sqrt(((ellipseRight_a * ellipseRight_a) + (ellipseLeft_a * ellipseLeft_a)) * ((ellipseRight_a * ellipseRight_a) + (ellipseLeft_a * ellipseLeft_a)) - 4 * (width_x * width_x)
            * ((ellipseRight_a * ellipseRight_a) + (ellipseLeft_a * ellipseLeft_a) - (width_x * width_x))))) / (2 * width_x*((ellipseLeft_a * ellipseLeft_a) - (ellipseRight_a * ellipseRight_a))));
        if (abs((int)x_plus) > abs((int)x_minus))
            x_answer = x_minus;
        else
            x_answer = x_plus;
    }
    y = sqrt(abs((int)(((ellipseRight_a * ellipseRight_a) - (width_x * width_x))*((ellipseRight_a * ellipseRight_a) - ((x_answer - width_x) * (x_answer - width_x))))))/ellipseRight_a;

    if(y >= HGL40DN1_TRIANGULATION_ERROR)
        y -= HGL40DN1_TRIANGULATION_ERROR;

	float dis = sqrt((x_answer * x_answer) + (y * y));

    //cout << "x : " << x_answer << " y : " << y << " dis : " << dis;

    return y;
}

double HGL40DN1Control::getDistance(int echoSensorN){
	int echoSensor_N = echoSensorN;
	if(echoSensor_N < 0)
		echoSensor_N = 0;
	else if(echoSensor_N >= getEchoSensorCount())
	{
		cout<<"존재하지 않는 수신 센서입니다. \n";
		return 0;
	}
	return pingMedian(5,echoSensor_N)/58;
}

double HGL40DN1Control::getTrigulation(void){
	if(getEchoSensorCount() != 2)
	{
		cout<<"수신 센서 개수가 2개이여야 합니다. \n";
		return 0;
	}
	else{
		float leftEllip_Distance, rightEllip_Distance;

		leftEllip_Distance = getDistance(0);
		rightEllip_Distance = getDistance(1);
		echoSensorWidth = getEchoSensorWidth();

		return triangulation_Cal(leftEllip_Distance,rightEllip_Distance,echoSensorWidth);
	}
}
