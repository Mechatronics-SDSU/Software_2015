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
    PACKETFRAMEID_GRABBERGET = 0x12,
    PACKETFRAMEID_TORPEDOGET = 0x13,
    PACKETFRAMEID_DROPPERGET = 0x14,
    PACKETFRAMEID_GRABBERSET = 0xB2,
    PACKETFRAMEID_TORPEDOSET = 0xB3,
    PACKETFRAMEID_DROPPERSET = 0xB4
};

enum PacketComStateEnum
{
    PACKETSTATE_READBYTECOUNT,
    PACKETSTATE_READFRAMEID,
    PACKETSTATE_PARSEGRABBERGET,
    PACKETSTATE_PARSETORPEDOGET,
    PACKETSTATE_PARSEDROPPERGET,
    PACKETSTATE_PARSEGRABBERSET,
    PACKETSTATE_PARSETORPEDOSET,
    PACKETSTATE_PARSEDROPPERSET
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
