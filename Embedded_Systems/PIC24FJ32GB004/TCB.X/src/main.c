/**
@author  Mechatronics RoboSub Team 2015
*/

// Includes
#include "system.h"        /* System funct/params, like osc/peripheral config */
#include "libpic30.h"      // Includes Delay Function
#include "crc.h"
#include "motorControl.h"
#include "circularBuffer.h"
#include "packetCom.h"
#include "packets.h"

// Defines
_CONFIG1(FWDTEN_OFF & JTAGEN_OFF)
//_CONFIG2(POSCMOD_HS & FNOSC_PRIPLL)
_CONFIG2(IESO_OFF & FNOSC_FRCPLL & OSCIOFNC_OFF & POSCMOD_NONE & PLL96MHZ_ON & PLLDIV_DIV2 & FCKSM_CSECME & IOL1WAY_OFF)

// Prototypes

// Variables
volatile uint32 msTicks = 0;
CircularBuffer* ReceiveBuffer;
CircularBuffer* TransmitBuffer;

/** Main function containing the background tasks.

@author Petar Tasev
*/
int16_t main(void)
{
    //uint8 arrayTest[8] = {8, 0xE1, 0, 0xFF, 1, 2, 3, 4};
    //uint8 arrayTest2[6] = {6, 1, 0x60, 0x84, 0x85, 0xEF};
    uint8 data = 20;
    volatile uint32 i;

    InitializeHardware();
    crcInit();

    //CircularBuffer_Write(ReceiveBuffer, arrayTest2, 6);

    while (1)
    {
        //for (i = 0; i < 32000; i++);
	PacketComState_Run();
        //CircularBuffer_Write(TransmitBuffer, &data, 1);

        //if (U2STAbits.TRMT == 1)
        //{
        //    IFS1bits.U2TXIF = 1;
        //}
    }
}
