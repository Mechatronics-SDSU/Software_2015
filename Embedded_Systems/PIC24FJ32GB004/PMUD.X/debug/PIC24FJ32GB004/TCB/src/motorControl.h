/**
@author  Mechatronics RoboSub Team 2015
@brief   Functions for controlling motor speed and direction
*/
#ifndef __motorControl__h
#define __motorControl__h

// Includes
#include "types.h"

// Defines
#define MOTOR_COUNT 4
#define MOTOR_RAMP_TIME_MS 5 ///< Period of motor pwm ramp

// Typedefs
typedef struct MotorStruct Motor;

// Structs
struct MotorStruct
{
    uint8 Id;
    int16 Velocity;
    int16 TargetVelocity;

    void (*UpdateVelocity)(Motor* const mtr);
};

// Prototypes
/** Allocate memory for a new Motor struct, and initialize it

@author Petar Tasev
*/
Motor* Motor_Create(void);
/** Initialize a given Motor struct

@param mtr Pointer to motor struct
@param UpdateVelocityFunc Pointer to function to set duty cycle and direction

@author Petar Tasev
*/
void Motor_Init(Motor* const mtr, void (*UpdateVelocityFunc)(Motor* const mtr));
/** Update the hardware PWM, and direction pin based on the Motor Velocity

@param mtr Pointer to the motor struct

@author Petar Tasev
*/
void Motor_UpdateVelocity(Motor* const mtr);
/** Ramps the motor up or down in relation to the target speed from the current.
It also changes the direction as needed.

@author Petar Tasev
*/
void RampMotors(void);
/** Set the target speed and direction of the motor in a buffer to be handled by RampMotors()

@param motorNum This is based on the frameID of the set motor packets.
@param direction The direction of the motor, can be [0, 1].
@param speed The speed of the motor in dutyCycle [0, 255].

@author Petar Tasev
*/
void SetMotorTarget(uint8 motorNum, uint8 direction, uint8 speed);

// Variables
extern Motor* motors[MOTOR_COUNT];

#endif
