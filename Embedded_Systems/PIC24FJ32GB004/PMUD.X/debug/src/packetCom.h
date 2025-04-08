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
    PACKETFRAMEID_DIRTYPOWGET = 0x25,
    PACKETFRAMEID_BATTERY1GET = 0x26,
    PACKETFRAMEID_BATTERY2GET = 0x27,
    PACKETFRAMEID_DIRTYPOWSET = 0xC5
};

enum PacketComStateEnum
{
    PACKETSTATE_READBYTECOUNT,
    PACKETSTATE_READFRAMEID,
    PACKETSTATE_PARSEDIRTYPOWGET,
    PACKETSTATE_PARSEBATTERY1GET,
    PACKETSTATE_PARSEBATTERY2GET,
    PACKETSTATE_PARSEDIRTYPOWSET
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
