// Includes
#include "system.h"
#include <uart.h>
#include "motorControl.h"

// Defines
#define OC2_IO  19
#define OC3_IO  20
#define OC4_IO  21
#define OC5_IO	22  // define OC5 output function number for PPS

#define PWM_FREQ 62500L
#define UART_BAUD 9600L

// Prototypes
static void MotorConfig(void);
static void TimeMsConfig(void);
static void UartConfig(void);

void InitializeHardware(void)
{
    ReceiveBuffer = CircularBuffer_Create();
    TransmitBuffer = CircularBuffer_Create();

    MotorConfig();
    TimeMsConfig();
    UartConfig();

    // Disable WatchDog Timer
    RCONbits.SWDTEN = 0;
    CLKDIVbits.CPDIV = 0;
    CLKDIVbits.RCDIV = 0;
#if 0

        /* Disable Watch Dog Timer */
        RCONbits.SWDTEN = 0;

        /* When clock switch occurs switch to Prim Osc (HS, XT, EC)with PLL */
        __builtin_write_OSCCONH(0x03);  /* Set OSCCONH for clock switch */
        __builtin_write_OSCCONL(0x01);  /* Start clock switching */
        while(OSCCONbits.COSC != 0b011);

        /* Wait for Clock switch to occur */
        /* Wait for PLL to lock, if PLL is used */
        /* while(OSCCONbits.LOCK != 1); */

#endif
}

void MotorConfig(void)
{
    // Initialize Motor Structures
    uint8 i;
    for (i = 0; i < MOTOR_COUNT; i++)
    {
	motors[i] = Motor_Create();
	motors[i]->Id = i;
    }

    // PWM output for motor power
    // I/O for direction pins
    /*
    Find the Period register value for a desired PWM frequency of 25 kHz,
    where Fosc = 8 MHz system clock
    Tcy = 2/Fosc = 250 ns
    PWM Period   =  1/PWM Frequency = 1/25 kHz = 40 us
    PWM Period   = (PR2 + 1) * Tcy * (Timer 2 Prescale Value)
    40 us = (PR2 + 1) * 250 ns * 1
    PR2 = 159
     */

    // Setup Pwm, and Direction bits to Output
    TRISCbits.TRISC4 = 0; // Set PORT C for Output Need C 4,6,8
    TRISCbits.TRISC6 = 0; // Set PORT A for Output Need A 9
    TRISBbits.TRISB8 = 0;
    TRISAbits.TRISA9 = 0;

    // Setup remappable pins to Output Compare
    RPOR9bits.RP19R = OC2_IO; // OC2 for PWM 1 (Pin 36)
    RPOR10bits.RP21R = OC3_IO; // OC3 for PWM 2 (Pin 38)
    RPOR11bits.RP23R = OC4_IO; // OC4 for PWM 3 (Pin 3)
    RPOR12bits.RP25R = OC5_IO; // OC5 for PWM 4 (Pin 5)

    // Set Output Comapre mode to Disabled during init
    OC5CON1bits.OCM = 0b000;
    OC4CON1bits.OCM = 0b000;
    OC3CON1bits.OCM = 0b000;
    OC2CON1bits.OCM = 0b000;

    // Ouput Compare Register setup Duty Cycle
    OC5R = 50;
    OC4R = 50;
    OC3R = 50;
    OC2R = 50;

    // Setup Output Compare frequency
    OC2RS = FCY / PWM_FREQ - 1;
    OC3RS = FCY / PWM_FREQ - 1;
    OC4RS = FCY / PWM_FREQ - 1;
    OC5RS = FCY / PWM_FREQ - 1;

    // Allow Output Compare to work when CPU is in Idle Mode
    OC5CON1bits.OCSIDL = 0;
    OC4CON1bits.OCSIDL = 0;
    OC3CON1bits.OCSIDL = 0;
    OC2CON1bits.OCSIDL = 0;

    // Set the PWM Fault pin to reset (Only Used if OCM == 111)
    OC5CON1bits.OCFLT = 0;
    OC4CON1bits.OCFLT = 0;
    OC3CON1bits.OCFLT = 0;
    OC2CON1bits.OCFLT = 0;

    // Set the Clock Source for the Output Compare (000 == Tim2)
    OC5CON1bits.OCTSEL = 0b000;
    OC4CON1bits.OCTSEL = 0b000;
    OC3CON1bits.OCTSEL = 0b000;
    OC2CON1bits.OCTSEL = 0b000;

    // Set Output Compare Mode to Edge-Aligned PWM mode
    OC5CON1bits.OCM = 0x6;
    OC4CON1bits.OCM = 0x6;
    OC3CON1bits.OCM = 0x6;
    OC2CON1bits.OCM = 0x6;

    // Setup Period Value Register of Tim2 with PWM frequency
    PR2 = FCY / PWM_FREQ - 1;//0x9F;

    // Clear Output Compare interrupt flag
    IFS0bits.T2IF = 0;
    IFS1bits.T4IF = 0;

    // Start Timer2 by setting the Timer On bit
    T2CONbits.TON = 1;
}

void TimeMsConfig(void)
{
    // Setup a 1 ms timer interrupt
    PR3 = 0x3E80;//0x1F40;//0xFA0;	 // Set to 4000 (0xFA0), since 4 MHz / 4k = 1kHz
    IPC2bits.T3IP = 5;	 // Set interrupt priority
    T3CONbits.TON = 1;	 // Turn on the Timer
    IFS0bits.T3IF = 0;	 // Reset interrupt flag
    IEC0bits.T3IE = 1;	 // Turn on the Timer3 interrupt
}

void UartConfig(void)
{
    // Set RP7 (Pin 43) to U2TX
    //TRISBbits.TRISB7 = 0;
    RPOR3bits.RP7R = 5;
    // Set RP8 (Pin 44) to U2RX
    RPINR19bits.U2RXR = 8;
    // Set RB8 (Pin 44) as Input
    TRISBbits.TRISB8 = 1;

    // Set Baud Rate to 9600
    U2BRG = FCY / 16 / UART_BAUD - 1;//0x19;

    // Allow operation in idle mode
    U2MODEbits.USIDL = 0;
    U2MODEbits.WAKE = 0;

    // Enable Uart 2
    U2MODEbits.UARTEN = 1;

    // Enable Interrupt when there is 1 space in the Tx Buffer
    U2STAbits.UTXISEL1 = 0;
    U2STAbits.UTXISEL0 = 0;
    // Enable Interrupt when Rx Buffer is not Empty
    U2STAbits.URXISEL = 0;

    // Enable Transmitter
    U2STAbits.UTXEN = 1;

    // Reset RX interrupt flag
    IFS1bits.U2RXIF = 0;
    // Reset TX interrupt flag
    IFS1bits.U2TXIF = 0;

    // Enable Tx Interrupt
    IEC1bits.U2TXIE = 1;
    // Enable Rx Interrupt
    IEC1bits.U2RXIE = 1;
}