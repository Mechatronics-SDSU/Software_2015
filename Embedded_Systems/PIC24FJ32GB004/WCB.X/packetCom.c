// Includes
#include "packetCom.h"
#include "circularBuffer.h"
#include "packets.h"
#include "crc.h"
#include <xc.h>
#include <stdlib.h>
#include "system.h"
#include "types.h"

// Variables
static PacketComState CurrentPacketComState;
static uint8 CurrentPacket[MAX_PACKET_BYTECOUNT] = {0};
static Packet* const DataPacket = (Packet*)&CurrentPacket[0];
static volatile uint8 CurrentPacketReadCount;

void PacketComState_Run(void)
{
    /*BYTECOUNT GET*/
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
    /*FRAMEID GET*/
    else if (PACKETSTATE_READFRAMEID == CurrentPacketComState)
    {
	if (CircularBuffer_Read(ReceiveBuffer, &CurrentPacket[1]))
	{
	    CurrentPacketComState = PacketComState_ParseFrameId();
	}
    }
    /*GRABBER GET*/
    else if (PACKETSTATE_PARSEGRABBERGET == CurrentPacketComState)
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

	    DataPacket->GrabberGet.Header.ByteCount = 7;
	    DataPacket->GrabberGet.ClawStatus = clawstatus;
	    DataPacket->GrabberGet.Crc = crcFast((uint8*)DataPacket, 3);
	    CircularBuffer_Write(TransmitBuffer, &CurrentPacket[0], 7);

	    CurrentPacketComState = PACKETSTATE_READBYTECOUNT;
	    if (U2STAbits.TRMT == 1)
            {
                IFS1bits.U2TXIF = 1;
            }
	}
    }
    /*TORPEDO GET*/
    else if (PACKETSTATE_PARSETORPEDOGET == CurrentPacketComState)
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

	    DataPacket->TorpedoGet.Header.ByteCount = 8;
            DataPacket->TorpedoGet.Torpedo1Status = torpedo1status;
            DataPacket->TorpedoGet.Torpedo2Status = torpedo2status;
	    DataPacket->TorpedoGet.Crc = crcFast((uint8*)DataPacket, 4);
	    CircularBuffer_Write(TransmitBuffer, &CurrentPacket[0], 8);

	    CurrentPacketComState = PACKETSTATE_READBYTECOUNT;
	    if (U2STAbits.TRMT == 1)
            {
                IFS1bits.U2TXIF = 1;
            }
	}
    }
    /*DROPPER GET*/
    else if (PACKETSTATE_PARSEDROPPERGET == CurrentPacketComState)
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

	    DataPacket->DropperGet.Header.ByteCount = 7;
            DataPacket->DropperGet.CurrentPWM = dropstatus;
	    DataPacket->DropperGet.Crc = crcFast((uint8*)DataPacket, 3);
	    CircularBuffer_Write(TransmitBuffer, &CurrentPacket[0], 7);

	    CurrentPacketComState = PACKETSTATE_READBYTECOUNT;
	    if (U2STAbits.TRMT == 1)
            {
                IFS1bits.U2TXIF = 1;
            }
	}
    }
    /*GRABBER SET*/
    else if (PACKETSTATE_PARSEGRABBERSET == CurrentPacketComState)
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

            // set the position of the grabber arm open or closed
            CLAW = DataPacket->GrabberSet.Grab;

	    CurrentPacketComState = PACKETSTATE_READBYTECOUNT;
	}
    }
    /*TORPEDOS SET*/
    else if (PACKETSTATE_PARSETORPEDOSET == CurrentPacketComState)
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

            // fire torpedo 1
            TORPEDO1 = DataPacket->TorpedoSet.Fire1;
            // fire torpedo 2
            TORPEDO2 = DataPacket->TorpedoSet.Fire2;

            CurrentPacketComState = PACKETSTATE_READBYTECOUNT;
	}
    }
    /*DROPPER SET*/
    else if (PACKETSTATE_PARSEDROPPERSET == CurrentPacketComState)
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

            // set the pwm for the dropper 0 drop 1, 90 normal, 180 drop 2
            DROP = DataPacket->DropperSet.SetPWM;

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
	if (PACKETFRAMEID_GRABBERGET == frameId)
	{
	    return PACKETSTATE_PARSEGRABBERGET;
	}
        else if (PACKETFRAMEID_TORPEDOGET == frameId)
	{
	    return PACKETSTATE_PARSETORPEDOGET;
	}
        else if (PACKETFRAMEID_DROPPERGET == frameId)
	{
	    return PACKETSTATE_PARSEDROPPERGET;
	}
	else
	{
	    return PACKETSTATE_READBYTECOUNT;
	}
    }
    else if (frameId > 0x9F) // Set
    {
	if (PACKETFRAMEID_GRABBERSET == frameId)
	{
	    return PACKETSTATE_PARSEGRABBERSET;
	}
        else if (PACKETFRAMEID_TORPEDOSET == frameId)
	{
	    return PACKETSTATE_PARSETORPEDOSET;
	}
        else if (PACKETFRAMEID_DROPPERSET == frameId)
	{
	    return PACKETSTATE_PARSEDROPPERSET;
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

