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

struct PacketGrabberGetStruct
{
    struct PacketHeaderStruct Header;
    uint8 ClawStatus;
    __pack uint32 Crc;
};

struct PacketTorpedoGetStruct
{
    struct PacketHeaderStruct Header;
    uint8 Torpedo1Status;
    uint8 Torpedo2Status;
    uint32 Crc;
};

struct PacketDropperGetStruct
{
    struct PacketHeaderStruct Header;
    uint8 CurrentPWM;
    __pack uint32 Crc;
};

struct PacketGrabberSetStruct
{
    struct PacketHeaderStruct Header;
    uint8 Grab;
    __pack uint32 Crc;
};

struct PacketTorpedoSetStruct
{
    struct PacketHeaderStruct Header;
    uint8 Fire1;
    uint8 Fire2;
    uint32 Crc;
};

struct PacketDropperSetStruct
{
    struct PacketHeaderStruct Header;
    uint8 SetPWM;
    __pack uint32 Crc;
};

union PacketUnion
{
    struct PacketHeaderStruct Header;
    struct PacketGrabberGetStruct GrabberGet;
    struct PacketTorpedoGetStruct TorpedoGet;
    struct PacketDropperGetStruct DropperGet;
    struct PacketGrabberSetStruct GrabberSet;
    struct PacketTorpedoSetStruct TorpedoSet;
    struct PacketDropperSetStruct DropperSet;
};

// Variables

// Prototypes

#endif
