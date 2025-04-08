// Includes
#include "packetCom.h"
#include "circularBuffer.h"
#include "packets.h"
#include "crc.h"
#include "motorControl.h"
#include <xc.h>
#include <stdlib.h>
#include "system.h"

// Variables
static PacketComState CurrentPacketComState;
static uint8 CurrentPacket[MAX_PACKET_BYTECOUNT] = {0};
static Packet* const DataPacket = (Packet*)&CurrentPacket[0];
static volatile uint8 CurrentPacketReadCount;

void PacketComState_Run(void)
{
    if (PACKETSTATE_READBYTECOUNT == CurrentPacketComState)
    {
	if (CircularBuffer_Read(ReceiveBuffer, &CurrentPacket[0]))
	{
	    if (CurrentPacket[0] > MAX_PACKET_BYTECOUNT || CurrentPacket[0] < MIN_PACKET_BYTECOUNT)
	    {
		return;
	    }

            CurrentPacketReadCount = 2;
	    CurrentPacketComState = PACKETSTATE_READFRAMEID;
	}
    }
    else if (PACKETSTATE_READFRAMEID == CurrentPacketComState)
    {
	if (CircularBuffer_Read(ReceiveBuffer, &CurrentPacket[1]))
	{
	    CurrentPacketComState = PacketComState_ParseFrameId();
	}
    }
    else if (PACKETSTATE_PARSEDEPTHGET == CurrentPacketComState)
    {
        CurrentPacketReadCount += CircularBuffer_ReadCopy(ReceiveBuffer,
                &CurrentPacket[CurrentPacketReadCount],
                CurrentPacket[0] - CurrentPacketReadCount);
	if (CurrentPacketReadCount == CurrentPacket[0])
	{
	    if (!PacketComState_CheckCRC())
	    {
		CurrentPacketComState = PACKETSTATE_READBYTECOUNT;
		return;
	    }

	    DataPacket->DepthGet.Header.ByteCount = 8;
	    //DataPacket->DepthGet.Header.FrameId = ;

	    DataPacket->DepthGet.Depth = 272;

	    DataPacket->DepthGet.Crc = crcFast(&CurrentPacket[0], 4);
	    CircularBuffer_Write(TransmitBuffer, &CurrentPacket[0], 8);

	    CurrentPacketComState = PACKETSTATE_READBYTECOUNT;
	    if (U2STAbits.TRMT == 1)
            {
                IFS1bits.U2TXIF = 1;
            }
	}
    }
    else if (PACKETSTATE_PARSEMOTORGET == CurrentPacketComState)
    {
        CurrentPacketReadCount += CircularBuffer_ReadCopy(ReceiveBuffer,
                &CurrentPacket[CurrentPacketReadCount],
                CurrentPacket[0] - CurrentPacketReadCount);
	if (CurrentPacketReadCount == CurrentPacket[0])
	{
	    if (!PacketComState_CheckCRC())
	    {
		CurrentPacketComState = PACKETSTATE_READBYTECOUNT;
		return;
	    }

	    DataPacket->MotorGet.Header.ByteCount = 10;
	    //DataPacket->DepthGet.Header.FrameId = ;

	    DataPacket->MotorGet.TargetDirection =
		    IS_NEGATIVE(motors[DataPacket->MotorGet.Header.FrameId - 1]->TargetVelocity);
	    DataPacket->MotorGet.TargetSpeed =
		    abs(motors[DataPacket->MotorGet.Header.FrameId - 1]->TargetVelocity);
	    DataPacket->MotorGet.CurrentDirection =
		    IS_NEGATIVE(motors[DataPacket->MotorGet.Header.FrameId - 1]->Velocity);
	    DataPacket->MotorGet.CurrentSpeed = 
		    abs(motors[DataPacket->MotorGet.Header.FrameId - 1]->Velocity);

	    DataPacket->MotorGet.Crc = crcFast(&CurrentPacket[0], 6);
	    CircularBuffer_Write(TransmitBuffer, &CurrentPacket[0], 10);

	    CurrentPacketComState = PACKETSTATE_READBYTECOUNT;
	    if (U2STAbits.TRMT == 1)
            {
                IFS1bits.U2TXIF = 1;
            }
	}
    }
    else if (PACKETSTATE_PARSEMOTORSET == CurrentPacketComState)
    {
        CurrentPacketReadCount += CircularBuffer_ReadCopy(ReceiveBuffer,
                &CurrentPacket[CurrentPacketReadCount],
                CurrentPacket[0] - CurrentPacketReadCount);
	if (CurrentPacketReadCount == CurrentPacket[0])
	{
	    if (!PacketComState_CheckCRC())
	    {
		CurrentPacketComState = PACKETSTATE_READBYTECOUNT;
		return;
	    }

	    SetMotorTarget(DataPacket->MotorSet.Header.FrameId,
		    DataPacket->MotorSet.Direction,
		    DataPacket->MotorSet.Speed);

	    CurrentPacketComState = PACKETSTATE_READBYTECOUNT;
	}
    }
    else
    {
	CurrentPacketComState = PACKETSTATE_READBYTECOUNT;
    }
}

PacketComState PacketComState_ParseFrameId(void)
{
    uint8 frameId = CurrentPacket[1];

    if (frameId < 0x70) // Get
    {
	if (PACKETFRAMEID_DEPTHGET == frameId)
	{
	    return PACKETSTATE_PARSEDEPTHGET;
	}
	else if (PACKETFRAMEID_MOTOR1GET <= frameId && PACKETFRAMEID_MOTOR6GET >= frameId)
	{
	    return PACKETSTATE_PARSEMOTORGET;
	}
	else
	{
	    return PACKETSTATE_READBYTECOUNT;
	}
    }
    else if (frameId > 0x9F) // Set
    {
	if ((PACKETFRAMEID_MOTOR1SET <= frameId && PACKETFRAMEID_MOTOR6SET >= frameId) ||
		(PACKETFRAMEID_MOTOR1A2SET <= frameId && PACKETFRAMEID_MOTOR5A6SET >= frameId))
	{
	    return PACKETSTATE_PARSEMOTORSET;
	}
	else
	{
	    return PACKETSTATE_READBYTECOUNT;
	}
    }
    else // Alert, not supposed to have
    {
	return PACKETSTATE_READBYTECOUNT;
    }
}

uint8 PacketComState_CheckCRC(void)
{
    uint32 calcedCRC = crcFast(&CurrentPacket[0], CurrentPacket[0] - 4);
    uint8 i = CurrentPacket[0] - 4;
    uint32 actualCRC;

    actualCRC = (uint32)CurrentPacket[i];
    actualCRC += (uint32)CurrentPacket[++i] << 8;
    actualCRC += (uint32)CurrentPacket[++i] << 16;
    actualCRC += (uint32)CurrentPacket[++i] << 24;
    
    return calcedCRC == actualCRC;
}
