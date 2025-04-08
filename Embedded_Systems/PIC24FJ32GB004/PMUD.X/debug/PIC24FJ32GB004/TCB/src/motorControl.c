// Includes
#include "motorControl.h"
#include <stdlib.h>
#include <xc.h>

// Variables
Motor* motors[MOTOR_COUNT];
static const uint8 directionPin[MOTOR_COUNT] = { 4, 4, 4, 4};
static volatile uint16* const directionReg[MOTOR_COUNT] = { &LATC, &LATC, &LATC, &LATC };
static volatile uint16* const dutyCycleReg[MOTOR_COUNT] = { &OC5R, &OC2R, &OC3R, &OC4R };

Motor* Motor_Create(void)
{
    Motor* mtr = (Motor*)malloc(sizeof(Motor));

    if (NULL != mtr)
    {
	Motor_Init(mtr, Motor_UpdateVelocity);
    }

    return mtr;
}

void Motor_Init(Motor* const mtr, void (*UpdateVelocityFunc)(Motor* const mtr))
{
    mtr->Id = 0;
    mtr->Velocity = 0;
    mtr->TargetVelocity = 0;
    mtr->UpdateVelocity = UpdateVelocityFunc;
}

void SetMotorTarget(uint8 motorNum, uint8 direction, uint8 speed)
{
	int motorIndex = motorNum - 0xE1;
	int duplicate = 0;
	if (motorIndex > 5)
	{
		motorIndex = (motorIndex - 9) * 2;
		duplicate = 1;
	}
	
	motors[motorIndex]->TargetVelocity = speed * (direction ? -1 : 1);
	
	if (duplicate)
	{
		SetMotorTarget(++motorNum, direction, speed);
	}
}

void RampMotors(void)
{
    uint8 i;

    for (i = 0; i < MOTOR_COUNT; i++)
    {
	if (motors[i]->Velocity < motors[i]->TargetVelocity)
	{
	    ++motors[i]->Velocity;
	}
	else if (motors[i]->Velocity > motors[i]->TargetVelocity)
	{
	    --motors[i]->Velocity;
	}
	else
	{
	    continue;
	}

	motors[i]->UpdateVelocity(motors[i]);
    }
}

void Motor_UpdateVelocity(Motor* const mtr)
{
    uint8 direction = IS_NEGATIVE(mtr->Velocity);
    if (direction == 1)
    {
	*directionReg[mtr->Id] |= (1 << directionPin[mtr->Id]);
	//LATCbits.LATC4 |= (1 << 7);
    }
    else if (direction == 0)
    {
	*directionReg[mtr->Id] &= ~(1 << directionPin[mtr->Id]);
	//LATCbits.LATC4 &= ~(1 << 7);
    }

    *dutyCycleReg[mtr->Id] = abs(mtr->Velocity);
    //*dutyCycleReg[mtr->Id + 1] = abs(mtr->Velocity);
}
