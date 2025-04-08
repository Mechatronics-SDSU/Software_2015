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

struct PacketSensorDataGetStruct
{
	struct PacketHeaderStruct Header;
	uint16 SensorData1;
	uint16 SensorData2;
	uint16 SensorData3;
	uint32 Crc;
};

union PacketUnion
{
    struct PacketHeaderStruct __pack Header;
    struct PacketSensorDataGetStruct __pack SensorDataGet;
};

// Variables

// Prototypes

#endif
