/**
@author  Mechatronics RoboSub Team 2015
@brief   Structures for all of the different data types
*/
#ifndef __packets__h
#define __packets__h

// Includes
#include "types.h"

// Defines
#define MAX_PACKET_BYTECOUNT 16
#define MIN_PACKET_BYTECOUNT 6

// Typedefs
typedef union PacketUnion Packet;

// Structures
struct PacketHeaderStruct
{
    uint8 ByteCount;
    uint8 FrameId;
};

struct PacketDirtyPowerGetStruct
{
	struct PacketHeaderStruct Header;
	uint8 Status;
	__pack uint32 Crc;
};

struct PacketBatteryInfoGetStruct
{
	struct PacketHeaderStruct Header;
	uint16 Voltage;
        uint16 Current;
	uint32 Crc;
};

union PacketUnion
{
    struct PacketHeaderStruct Header;
    struct PacketDirtyPowerGetStruct DirtyPowerGet;
    struct PacketBatteryInfoGetStruct BatteryInfoGet;
};

// Variables

// Prototypes

#endif
