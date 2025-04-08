// Includes
#include "packetCom.h"
#include "circularBuffer.h"
#include "packets.h"
#include "crc.h"
#include <xc.h>
#include <stdlib.h>
#include "system.h"

// Prototypes
uint16 GetSensorMedian(uint8 a, uint8 b, uint8 c);

// Variables
static PacketComState CurrentPacketComState;
static uint8 CurrentPacket[MAX_PACKET_BYTECOUNT] = { 0 };
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
        else if (PACKETSTATE_PARSEINTTEMPGET == CurrentPacketComState)
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

			DataPacket->SensorDataGet.Header.ByteCount = 12;
			DataPacket->SensorDataGet.SensorData1 = AdcValues[0];
			DataPacket->SensorDataGet.SensorData2 = AdcValues[1];
			DataPacket->SensorDataGet.SensorData3 = AdcValues[8];
			DataPacket->SensorDataGet.Crc = crcFast((uint8*)DataPacket, 8);
			CircularBuffer_Write(TransmitBuffer, &CurrentPacket[0], 12);

			CurrentPacketComState = PACKETSTATE_READBYTECOUNT;
			if (U2STAbits.TRMT == 1)
			{
				IFS1bits.U2TXIF = 1;
			}
		}
	}
        else if (PACKETSTATE_PARSEINTPRESGET == CurrentPacketComState)
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

			DataPacket->SensorDataGet.Header.ByteCount = 12;
			DataPacket->SensorDataGet.SensorData1 = AdcValues[5];
			DataPacket->SensorDataGet.SensorData2 = AdcValues[6];
			DataPacket->SensorDataGet.SensorData3 = AdcValues[7];
			DataPacket->SensorDataGet.Crc = crcFast((uint8*)DataPacket, 8);
			CircularBuffer_Write(TransmitBuffer, &CurrentPacket[0], 12);

			CurrentPacketComState = PACKETSTATE_READBYTECOUNT;
			if (U2STAbits.TRMT == 1)
			{
				IFS1bits.U2TXIF = 1;
			}
		}
	}
	else if (PACKETSTATE_PARSEEXTPRESGET == CurrentPacketComState)
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

			DataPacket->SensorDataGet.Header.ByteCount = 12;
			DataPacket->SensorDataGet.SensorData1 = AdcValues[2];
			DataPacket->SensorDataGet.SensorData2 = AdcValues[3];
			DataPacket->SensorDataGet.SensorData3 = AdcValues[4];
			DataPacket->SensorDataGet.Crc = crcFast((uint8*)DataPacket, 8);
			CircularBuffer_Write(TransmitBuffer, &CurrentPacket[0], 12);

			CurrentPacketComState = PACKETSTATE_READBYTECOUNT;
			if (U2STAbits.TRMT == 1)
			{
				IFS1bits.U2TXIF = 1;
			}
		}
	}
	else
	{
		CurrentPacketComState = PACKETSTATE_READBYTECOUNT;
	}
}

uint16 GetSensorMedian(uint8 a, uint8 b, uint8 c)
{
	if (a < b)
	{
		// partial order = a,b
		if (b < c)
		{
			// 2 comparisons: order is a,b,c
			return AdcValues[b];
		}
		else
		{
			// order is a,c,b or c,a,b
			if (a < c)
			{
				// order is a,c,b -- 3 comparisons
				return AdcValues[c];
			}
			else
			{
				// order is c,a,b -- 3 comparisons
				return AdcValues[a];
			}
		}
	}
	else
	{
		// partial order = b,a  
		if (c < b)
		{
			// 2 comparisons: order is c,b,a
			return AdcValues[b];
		}
		else
		{
			// order is b,c,a or b,a,c
			if (c > a)
			{
				// order is b,a,c -- 3 comparisons
				return AdcValues[a];
			}
			else
			{
				// order is b,c,a -- 3 comparisons
				return AdcValues[c];
			}
		}
	}
}

PacketComState PacketComState_ParseFrameId(void)
{
	uint8 frameId = CurrentPacket[1];

	if (frameId < 0x70) // Get
	{
		if (PACKETFRAMEID_INTTEMPGET == frameId)
		{
			return PACKETSTATE_PARSEINTTEMPGET;
		}
                else if (PACKETFRAMEID_INTPRESGET == frameId)
		{
			return PACKETSTATE_PARSEINTPRESGET;
		}
                else if (PACKETFRAMEID_EXTPRESGET == frameId)
		{
			return PACKETSTATE_PARSEEXTPRESGET;
		}
		else
		{
			return PACKETSTATE_READBYTECOUNT;
		}
	}
	else if (frameId > 0x9F) // Set
	{
		return PACKETSTATE_READBYTECOUNT;
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
