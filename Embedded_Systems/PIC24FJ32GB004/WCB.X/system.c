// Includes
#include "system.h"
#include <uart.h>

// Defines
#define UART_BAUD 9600L

// Prototypes
static void TimeMsConfig(void);
static void UartConfig(void);

void InitializeHardware(void)
{
    ReceiveBuffer = CircularBuffer_Create();
    TransmitBuffer = CircularBuffer_Create();

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
    RPOR11bits.RP23R = 5;
    TRISCbits.TRISC7 = 0;
    // Set RP8 (Pin 44) to U2RX
    RPINR19bits.U2RXR = 22;
    // Set RB8 (Pin 44) as Input
    TRISCbits.TRISC6 = 1;

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