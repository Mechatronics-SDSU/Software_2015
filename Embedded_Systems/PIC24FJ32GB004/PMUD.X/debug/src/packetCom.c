// Includes
#include "packetCom.h"
#include "circularBuffer.h"
#include "packets.h"
#include "crc.h"
#include <xc.h>
#include <stdlib.h>
#include "system.h"
#include "austins_PIC24FJ32GB004_lib.h"

// Prototypes

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
        else if (PACKETSTATE_PARSEDIRTYPOWGET == CurrentPacketComState)
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

			DataPacket->DirtyPowerGet.Header.ByteCount = 7;
			DataPacket->DirtyPowerGet.Status = ONLINE;
			DataPacket->DirtyPowerGet.Crc = crcFast((uint8*)DataPacket, 3);
			CircularBuffer_Write(TransmitBuffer, &CurrentPacket[0], 7);

			CurrentPacketComState = PACKETSTATE_READBYTECOUNT;
			if (U2STAbits.TRMT == 1)
			{
				IFS1bits.U2TXIF = 1;
			}
		}
	}
        else if (PACKETSTATE_PARSEBATTERY1GET == CurrentPacketComState)
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

			DataPacket->BatteryInfoGet.Header.ByteCount = 10;
			DataPacket->BatteryInfoGet.Voltage = voltage1;
                        DataPacket->BatteryInfoGet.Current = delta1;
			DataPacket->BatteryInfoGet.Crc = crcFast((uint8*)DataPacket, 6);
			CircularBuffer_Write(TransmitBuffer, &CurrentPacket[0], 10);

			CurrentPacketComState = PACKETSTATE_READBYTECOUNT;
			if (U2STAbits.TRMT == 1)
			{
				IFS1bits.U2TXIF = 1;
			}
		}
	}
        else if (PACKETSTATE_PARSEBATTERY2GET == CurrentPacketComState)
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

			DataPacket->BatteryInfoGet.Header.ByteCount = 10;
			DataPacket->BatteryInfoGet.Voltage = voltage2;
                        DataPacket->BatteryInfoGet.Current = delta2;
			DataPacket->BatteryInfoGet.Crc = crcFast((uint8*)DataPacket, 6);
			CircularBuffer_Write(TransmitBuffer, &CurrentPacket[0], 10);

			CurrentPacketComState = PACKETSTATE_READBYTECOUNT;
			if (U2STAbits.TRMT == 1)
			{
				IFS1bits.U2TXIF = 1;
			}
		}
	}
        else if (PACKETSTATE_PARSEDIRTYPOWSET == CurrentPacketComState)
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

			OFFLINE = !DataPacket->DirtyPowerGet.Status;
            if (DataPacket->DirtyPowerGet.Status == 1)
            {
                PRE_ARM = DataPacket->DirtyPowerGet.Status;
                reset = !DataPacket->DirtyPowerGet.Status;
            }
            else
            {
                ONLINE = DataPacket->DirtyPowerGet.Status;
            }
			
                        

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
		if (PACKETFRAMEID_DIRTYPOWGET == frameId)
		{
			return PACKETSTATE_PARSEDIRTYPOWGET;
		}
                else if (PACKETFRAMEID_BATTERY1GET == frameId)
		{
			return PACKETSTATE_PARSEBATTERY1GET;
		}
                else if (PACKETFRAMEID_BATTERY2GET == frameId)
		{
			return PACKETSTATE_PARSEBATTERY2GET;
		}
		else
		{
			return PACKETSTATE_READBYTECOUNT;
		}
	}
	else if (frameId > 0x9F) // Set
	{
            	if (PACKETFRAMEID_DIRTYPOWSET == frameId)
		{
                    return PACKETSTATE_PARSEDIRTYPOWSET;
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
