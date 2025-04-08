/**
@author  Mechatronics RoboSub Team 2015
@brief   Handler for main communication states, and data
*/
#ifndef __packetCom__h
#define __packetCom__h

// Includes
#include "types.h"

// Defines

// Typdefs
typedef enum PacketComStateEnum PacketComState;
typedef enum PacketFrameIdEnum PacketComFrameId;

// Structs
enum PacketFrameIdEnum
{
    PACKETFRAMEID_DEPTHGET,
    PACKETFRAMEID_MOTOR1GET,
    PACKETFRAMEID_MOTOR6GET = 0x6,
    PACKETFRAMEID_MOTOR1SET = 0xE1,
    PACKETFRAMEID_MOTOR6SET = 0xE6,
    PACKETFRAMEID_MOTOR1A2SET = 0xEA,
    PACKETFRAMEID_MOTOR5A6SET = 0xEC
};

enum PacketComStateEnum
{
    PACKETSTATE_READBYTECOUNT,
    PACKETSTATE_READFRAMEID,
    PACKETSTATE_PARSEDEPTHGET,
    PACKETSTATE_PARSEMOTORGET,
    PACKETSTATE_PARSEMOTORSET
};

// Variables

// Prototypes
/** Runs the state machine for the main communication

@author Petar Tasev
*/
void PacketComState_Run(void);

/** Analyzes the current packet frame id to decide on the next state

@return Returns the next state based on the frame id

@author Petar Tasev
*/
PacketComState PacketComState_ParseFrameId(void);

/** Checks the CRC of the received current packet against a calculated one

@return Returns 1 if the CRC is correct, or 0 if different

@author Petar Tasev
*/
uint8 PacketComState_CheckCRC(void);

#endif
