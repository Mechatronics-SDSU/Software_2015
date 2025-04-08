/**
@author  Mechatronics RoboSub Team 2015
*/

// Includes
#include "system.h"        /* System funct/params, like osc/peripheral config */
#include "libpic30.h"      // Includes Delay Function
#include "crc.h"
#include "circularBuffer.h"
#include "packetCom.h"
#include "packets.h"

// Defines
_CONFIG1(FWDTEN_OFF & JTAGEN_OFF)
//_CONFIG2(POSCMOD_HS & FNOSC_PRIPLL)
_CONFIG2(IESO_OFF  & OSCIOFNC_OFF & POSCMOD_NONE & PLL96MHZ_ON & PLLDIV_DIV2 & FCKSM_CSECME & IOL1WAY_OFF & FNOSC_FRCPLL)

// Prototypes
static void PWMConfig(void);

// Variables
volatile uint32 msTicks = 0;
CircularBuffer* ReceiveBuffer;
CircularBuffer* TransmitBuffer;

bool CLAW = 1;
uint8 TORPEDO1;
uint8 TORPEDO2;
uint8 DROP = 0xFF;
bool clawstatus;
bool torpedo1status;
bool torpedo2status;
uint8 dropstatus;

/* Main function containing the background tasks.*/

int16_t main(void)
{
    TRISBbits.TRISB3 = 0; // pin 24 output (torpedo 1)
    TRISBbits.TRISB2 = 0; // pin 23 output (torpedo 2)
    TRISCbits.TRISC2 = 0; // pin 27 output (dropper)
    TRISCbits.TRISC1 = 0; // pin 26 output (claw open)
    TRISCbits.TRISC0 = 0; // pin 25 output (claw close)
    //RPOR9bits.RP18R = 22; // PPS for output compare dropper
    RPOR1bits.RP3R = 22;    // PPS for output compare torpedo 1

    

    InitializeHardware();
    crcInit();
    PWMConfig();


    while(1)
    {
        PacketComState_Run();

        //Torpedo LED test
        //__delay_ms(2000);
        //LATBbits.LATB2 = 1;
        //LATBbits.LATB3 = 0;
        //__delay_ms(2000);
        //LATBbits.LATB2 = 0;
        //LATBbits.LATB3 = 1;
        //__delay_ms(2000);


        /****** Grabber ******/
        if (CLAW == 1)
        {
            // open claw
            // set claw open latch low and closed latched high
            LATCbits.LATC1 = 0; // pin 26
            LATCbits.LATC0 = 1; // pin 25
            clawstatus = 1; // claw status open
        }
        else
        {
            // default close claw
            // set claw closed latch low and open latch high
            LATCbits.LATC1 = 1; // pin 26
            LATCbits.LATC0 = 0; // pin 25
            clawstatus = 0; // claw status closed
        }

        /****** Torpedos ******/
        if (TORPEDO1 == 0xF1 && TORPEDO2 != 0x2F)
        {
            // fire torpedo 1
            // torpedo 1 latch high and torpedo 2 latch low
            //LATBbits.LATB3 = 0; // pin 24
            //LATBbits.LATB2 = 1; // pin 23
            //__delay_ms(1000);
            //LATBbits.LATB3 = 1; // pin 24
            torpedo1status = 0;
        }
        else if (TORPEDO1 != 0xF1 && TORPEDO2 == 0x2F)
        {
            // fire torpedo 2
            // torpedo 1 latch low and torpedo 2 latch high
            //LATBbits.LATB3 = 1; // pin 24
            //LATBbits.LATB2 = 0; // pin 23
            //__delay_ms(1000);
            //LATBbits.LATB2 = 1; // pin 23
            //torpedo2status = 0;
        }
        else
        {
            // default both torpedos loaded
            // torpedo 1 low, torpedo 2 low
            //LATBbits.LATB3 = 1; // pin 24
            //LATBbits.LATB2 = 1; // pin 23
            torpedo1status = 1;
            torpedo2status = 1;
        }

        /****** Dropper ******/
        // PR2(4999) * ( Pulse Period / PWM Period ) = Pulse Time but in hex (OC5R)

        OC5R = 0x1210;       // 1.5ms Period @ 0 deg  (375)
        __delay_ms(2000);
        OC5R = 0x1116;       // 2.5ms Period @ +90 deg  (625)
        __delay_ms(2000);
        OC5R = 0x12F1;        // 0.6ms Period @ -90 deg  (150)
        __delay_ms(2000);

        
//        if (DROP ==  0x00)
//        {
//            // Drop 1, 0.6ms @ -90 degrees
//            // drop servo pin 27
//            OC5R = 0x12F1; // (4849)
//            dropstatus = 0x00;
//        }
//        else if (DROP == 0xFF)
//        {
//            // Drop 2, 2.5ms @ +90 degrees
//            // drop servo pin 27
//            OC5R = 0x1116; // (4374)
//            dropstatus = 0xFF;
//        }
//        else
//        {
//            // default normal, 1.5ms @ 0 degrees
//            // drop servo pin 27
//            OC5R = 0x1210; // (4624)
//            dropstatus = 0x7F;
//        }
    }
}

void PWMConfig(void)
{
    /* where Fosc = 32MHz system clock
     * Tcy = 2/Fosc = 62.5ns
     * PWM Period = 20ms
     * PWM Period = (PR2 + 1) * Tcy * (Timer 2 Prescale Value)
     * 20ms = (PR2 + 1) * 62.5ns * 64
     * PR2 = 4999
     */
    OC5CON1bits.OCM = 0b0000;     // Disable OC5 until initialization
    OC5R = 0x3F;      // Timer Reload value for Duty Cycle (Starting Pulse)
    OC5CON1bits.OCTSEL = 0b000;  // Period Reload Clock Select for Timer 2
    OC5CON1bits.OCM = 0x6;  // Enable OC for Edge Aligned PWM
    PR2 = 0x1387;        // Timer 2 Reload Value for Period (4999)
    T2CONbits.TCKPS = 0b10;     // Timer 2 Clock Prescaler to 1:64
    T2CONbits.TON = 0b0001;  // Enable Timer 2
}
