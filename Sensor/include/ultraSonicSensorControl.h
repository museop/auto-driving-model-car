#include <time.h>
#include <sys/time.h>
#include <sys/msg.h>
#include <sys/ipc.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <jetsonGPIO.h>
#include <iostream>
#include <list>


#ifndef ULTRA_SONIC_SENSOR_CONTROL_H_
#define ULTRA_SONIC_SENSOR_CONTROL_H_

using namespace std;

#define SENSOR_END			4514

#define TRIG_MSG_TYPE		1
#define ECHO_MSG_TYPE		2
#define RESULT_MSG_TYPE   	3
#define ECHO_END_MSG_TYPE	4
#define TRIG_END_MSG_TYPE	5

#define ROUNDTRIP_CM        	58 

#define NO_ECHO             	0

#define MSG_CODE_INTERVAL	6

enum trigReady{
	READY = 1,
	NOTREADY = 0
};

typedef struct msgq_ultrasonic_sensor_timeval_data{
	long type;
	timeval timeval_data;
}uSonicTvalMsg;

typedef struct msgq_ultrasonic_sensor_end{
	long type;
	int msg_end;
}uSonicEndMsg;

typedef struct msgq_ultrasonic_trig_start{
	long type;
	trigReady trig_ready;
}uSonicTrigMsg;

typedef struct ultrasonic_trig_thread_arg_data{
	jetsonGPIO sensorGPIO;
	int sensorNumber;
	int uSonicEchoSensorCount;
}uSonicTrigTArg;

typedef struct ultrasonic_echo_thread_arg_data{
	jetsonGPIO sensorGPIO;
	int sensorNumber;
	int uSonicEchoSensorN;
	long maxSensorDelay;
	long maxSensorDistance;
	long sonicMakeDelay;
}uSonicEchoTArg;

#endif


	
