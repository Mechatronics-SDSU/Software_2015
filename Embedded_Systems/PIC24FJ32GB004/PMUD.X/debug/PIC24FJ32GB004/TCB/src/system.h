/**
@author  Mechatronics RoboSub Team 2015
@brief   System level defines, variables, and hardware setup
*/
#ifndef __system__h
#define __system__h

// Includes
#if defined(__XC16__)
    #include <xc.h>
#elif defined(__C30__)
    #if defined(__PIC24E__)
    	#include <p24Exxxx.h>
    #elif defined (__PIC24F__)||defined (__PIC24FK__)
	#include <p24Fxxxx.h>
    #elif defined(__PIC24H__)
	#include <p24Hxxxx.h>
    #endif
#endif

#include <stdbool.h>         /* For true/false definition */
#include "types.h"
#include "circularBuffer.h"

// Defines
#define SYS_FREQ        32000000L//8000000L
#define FCY             SYS_FREQ/2

// Variables
extern volatile uint32 msTicks;
extern CircularBuffer* ReceiveBuffer;
extern CircularBuffer* TransmitBuffer;

// Prototypes
void InitializeHardware(void);

#endif
