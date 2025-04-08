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
#include "austins_PIC24FJ32GB004_lib.h"

// Defines
_CONFIG1(FWDTEN_OFF & JTAGEN_OFF)
//_CONFIG2(POSCMOD_HS & FNOSC_PRIPLL)
_CONFIG2(IESO_OFF & FNOSC_FRCPLL & OSCIOFNC_OFF & POSCMOD_NONE & PLL96MHZ_ON & PLLDIV_DIV2 & FCKSM_CSECME & IOL1WAY_OFF)

// Prototypes
//Resets the I2C bus to Idle
void reset_i2c_bus(void)
{
   int x = 0;

   //initiate stop bit
   I2C1CONbits.PEN = 1;

   //wait for hardware clear of stop bit
   while (I2C1CONbits.PEN)
   {
      __delay_us(1);
      x ++;
      if (x > 20) break;
   }
   I2C1CONbits.RCEN = 0;
   IFS1bits.MI2C1IF = 0; // Clear Interrupt
   I2C1STATbits.IWCOL = 0;
   I2C1STATbits.BCL = 0;
   __delay_us(10);
}

//function initiates I2C1 module to baud rate BRG
void i2c_init(int BRG)
{
   int temp;

   // I2CBRG = 194 for 10Mhz OSCI with PPL with 100kHz I2C clock
   I2C1BRG = BRG;
   I2C1CONbits.I2CEN = 0;	// Disable I2C Mode
   //I2C1CONbits.DISSLW = 1;	// Disable slew rate control
   IFS1bits.MI2C1IF = 0;	 // Clear Interrupt
   I2C1CONbits.I2CEN = 1;	// Enable I2C Mode
   temp = I2C1RCV;	 // read buffer to clear buffer full
   reset_i2c_bus();	 // set bus to idle
}

//function iniates a start condition on bus
void i2c_start(void)
{
   int x = 0;
   I2C1CONbits.ACKDT = 0;	//Reset any previous Ack
   __delay_us(10);
   I2C1CONbits.SEN = 1;	//Initiate Start condition
   Nop();

   //the hardware will automatically clear Start Bit
   //wait for automatic clear before proceding
   while (I2C1CONbits.SEN)
   {
      __delay_us(1);
      x++;
      if (x > 20)
      break;
   }
   __delay_us(2);
}

void i2c_restart(void)
{
   int x = 0;

   I2C1CONbits.RSEN = 1;	//Initiate restart condition
   Nop();

   //the hardware will automatically clear restart bit
   //wait for automatic clear before proceding
   while (I2C1CONbits.RSEN)
   {
      __delay_us(1);
      x++;
      if (x > 20)	break;
   }

   __delay_us(2);
}

//basic I2C byte send
char send_i2c_byte(int data)
{
   int i;

   while (I2C1STATbits.TBF) { } // if a transmit is in progress, wait
   IFS1bits.MI2C1IF = 0; // Clear Interrupt
   I2C1TRN = data; // load the outgoing data byte

   // wait for transmission
   for (i=0; i<500; i++)
   {
      if (!I2C1STATbits.TRSTAT) break;
      __delay_us(1);

      }
      if (i == 500) {
      return(1);
   }

   // Check for ACK from slave, abort if not found
   if (I2C1STATbits.ACKSTAT == 1)
   {
       // if no acknowledge was found turn on LED
       //PIN8_LAT = OFF;
       return(1);
   }
   // if the slave acknowledge the LED will turn on
   //else PIN8_LAT = ON;

   __delay_us(2);
   return(0);
}

//function reads data, returns the read data, no ack
int8_t i2c_read(void)
{
   int i = 0;
   int8_t data = 0;

   //set I2C module to receive
   I2C1CONbits.RCEN = 1;

   //if no response, break
   while (!I2C1STATbits.RBF)
   {
      i ++;
      if (i > 2000) break;
   }

   //get data from I2CRCV register
   data = I2C1RCV;

   //return data
   return data;
}

//function reads data, returns the read data, with ack
char i2c_read_ack(void)	//does not reset bus!!!
{
   int i = 0;
   char data = 0;

   //set I2C module to receive
   I2C1CONbits.RCEN = 1;

   //if no response, break
   while (!I2C1STATbits.RBF)
   {
      i++;
      if (i > 2000) break;
   }

   //get data from I2CRCV register
   data = I2C1RCV;

   //set ACK to high
   I2C1CONbits.ACKEN = 1;

   //wait before exiting
   __delay_us(10);

   //return data
   return data;
}

void I2Cwrite(char addr, char subaddr, char value)
{
   i2c_start();
   send_i2c_byte(addr);
   send_i2c_byte(subaddr);
   send_i2c_byte(value);
   reset_i2c_bus();
}

int8_t I2Cread(char addr, char subaddr)
{
   int8_t temp;

   i2c_start();
   send_i2c_byte(addr);
   send_i2c_byte(subaddr);
   __delay_us(10);

   i2c_restart();
   send_i2c_byte(addr | 0x01);
   temp = i2c_read();

   reset_i2c_bus();
   return temp;
}

// Variables
volatile uint32 msTicks = 0;
CircularBuffer* ReceiveBuffer;
CircularBuffer* TransmitBuffer;
bool armed = OFF;         // State of Switches
extern bool reset = OFF;

extern bool OFFLINE = ON;       // States of Operation, start up OFFLINE
bool STANDBY = OFF;
extern bool PRE_ARM = OFF;
extern bool ONLINE = OFF;
bool PC_OK = ON;

bool armedSave = OFF;     // Temp variable for error checking
bool resetSave = OFF;

unsigned int armedCount = 0;    // Count of read switch states
unsigned int resetCount = 0;

int16_t v1inlsb = 0;
int16_t v1inmsb = 0;
int16_t v2inlsb = 0;
int16_t v2inmsb = 0;

int16_t delta_sense1_lsb = 0;
int16_t delta_sense1_msb = 0;
int16_t delta_sense2_lsb = 0;
int16_t delta_sense2_msb = 0;

extern int16_t voltage1 = 0;
extern int16_t voltage2 = 0;
extern int16_t delta1 = 0;
extern int16_t delta2 = 0;

/** Main function containing the background tasks.

@author Petar Tasev
*/
int16_t main(void)
{
    //uint8 arrayTest[8] = {8, 0xE1, 0, 0xFF, 1, 2, 3, 4};
    //uint8 arrayTest2[6] = {6, 1, 0x60, 0x84, 0x85, 0xEF};

    InitializeHardware();
    crcInit();

    //CircularBuffer_Write(ReceiveBuffer, arrayTest2, 6);

    I2C1CONbits.I2CEN = 1; //I2C Enable
    //IEC1bits.MI2C1IE = 1;  //Enable Master I2C Interrupt
    //I2C1BRG = 157;
    i2c_init(100); // Baud rate seems to only work for 19 and above, so i left it at 100 and it works fine

    /* Initialize IO ports and peripherals */
    PIN3_TRIS = INPUT; // ARMED input
    PIN4_TRIS = OUTPUT; // output pin to digital relay
    PIN5_TRIS = INPUT; // RESET input


    // Define Relay Off

    PIN4_LAT = OFF;

    while(1)
    {
        PacketComState_Run();
        /* Turning the sub back on
         * ----------------------------
         *Sub starts offline
         * 1) armed off and reset off
         * 2) armed off and reset on
         * 3) armed on and reset on
         * 4) armed on and reset off  ---> Sub comes online
         */

/******************************************************************************/
/*                 READ VALUES FROM SWITCHES                                  */
/******************************************************************************/

        __delay_ms(10);         // Set sample rate for reading Kill and Reset Switch



        if ( armedSave == PORTCbits.RC7 )
        {      // Read Value 25 more times

              armedCount++;

             if ( armedCount > 24 )
             {       // If read correctly 25 times change armed value

                 armed = armedSave;
                 armedCount = 0;

             }

         }

        else
        {

          armedSave = PORTCbits.RC7;     // Read Value from Kill / Arm Switch

          armedCount = 0;


        }


          if ( resetSave == PORTCbits.RC9 )
        {      // Read Value 25 more times

              resetCount++;

             if ( resetCount > 24 )
             {       // If read correctly 25 times change armed value

                 reset = resetSave;
                 resetCount = 0;

             }

         }

        else
        {

          resetSave = PORTCbits.RC9;     // Read Value from Reset Switch

          resetCount = 0;

        }
/******************************************************************************/
/*                 CHANGE OPERATIONAL MODE                                    */
/******************************************************************************/

        /* OFFLINE - weapons and motors are off, start with armed off and reset off*/
        /*
        if ( ((OFFLINE ^ ONLINE ) == 0) ) {

            // Check for exclusive state, OFFLINE if False, PRE ARM and STANDYBY fix themselves

            OFFLINE = ON;
            ONLINE = OFF;
            STANDBY = OFF;
            PRE_ARM = OFF;

        }

*/

        if ( ONLINE == ON )
        {

            if ( armed == OFF ) {

                OFFLINE = ON;
                ONLINE = OFF;
                STANDBY = OFF;
                PRE_ARM = OFF;
            }
        }

        else if( OFFLINE == ON )
        {
            // turn off digital relay
            PIN4_LAT = OFF;

            if ( reset == ON && armed == OFF ) {

                STANDBY = ON;
                OFFLINE = OFF;
                ONLINE = OFF;
                PRE_ARM = OFF;
            }

        }
        /* STANDBY */
        else if( STANDBY == ON )
        {

            if ( armed == ON && reset == ON )   {

                PRE_ARM = ON;
                STANDBY = OFF;
                OFFLINE = OFF;
                ONLINE = OFF;
            }

        }
        /* PRE ARM */
        else if( PRE_ARM == ON )
        {
            // need to send "ready to come online" to PC
            if ( armed == ON && reset == OFF && PC_OK == ON) {

                OFFLINE = OFF;
                STANDBY = OFF;
                PRE_ARM = OFF;
                ONLINE = ON;

                PIN4_LAT = ON;      // Turn Relay On

                /* ONLINE - weapons and motors are on, end with armed on and reset off */
            }


        }

        v1inlsb = I2Cread(0xDE, 0x1F);
        v1inmsb = I2Cread(0xDE, 0x1E);
        voltage1 = (v1inmsb << 8) | (v1inlsb & 0x00FF);

        v2inlsb = I2Cread(0xD4, 0x1F);
        v2inmsb = I2Cread(0xD4, 0x1E);
        voltage2 = (v2inmsb << 8) | (v2inlsb & 0x00FF);

        delta_sense1_lsb = I2Cread(0xDE, 0x15);
        delta_sense1_msb = I2Cread(0xDE, 0x14);
        delta1 = (delta_sense1_msb << 8) | (delta_sense1_lsb & 0x00FF);

        delta_sense2_lsb = I2Cread(0xD4, 0x15);
        delta_sense2_msb = I2Cread(0xD4, 0x14);
        delta2 = (delta_sense2_msb << 8) | (delta_sense2_lsb & 0x00FF);

    }
}
