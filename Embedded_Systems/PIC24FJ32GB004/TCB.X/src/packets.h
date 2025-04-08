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

struct PacketDepthGetStruct
{
    struct PacketHeaderStruct Header;
    uint16 Depth;
    uint32 Crc;
};

struct PacketMotorGetStruct
{
    struct PacketHeaderStruct Header;
    uint8 TargetDirection;
    uint8 CurrentDirection;
    uint8 TargetSpeed;
    uint8 CurrentSpeed;
    uint16 Current; // amps
    uint32 Crc;
};

struct PacketMotorSetStruct
{
    struct PacketHeaderStruct Header;
    uint8 Direction;
    uint8 Speed;
    uint32 Crc;
};

union PacketUnion
{
    struct PacketHeaderStruct __pack Header;
    struct PacketDepthGetStruct __pack DepthGet;
    struct PacketMotorGetStruct __pack MotorGet;
    struct PacketMotorSetStruct __pack MotorSet;
};

// Variables

// Prototypes

#endif
