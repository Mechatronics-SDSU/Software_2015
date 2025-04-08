// Includes
#include "system.h"
#include <uart.h>

// Defines
#define UART_BAUD 9600L

// Prototypes
static void SensorAdcConfig(void);
static void TimeMsConfig(void);
static void UartConfig(void);

void InitializeHardware(void)
{
    ReceiveBuffer = CircularBuffer_Create();
    TransmitBuffer = CircularBuffer_Create();

	SensorAdcConfig();
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

void SensorAdcConfig(void)
{
	// 4, 5, 6, 7, 8, 9, 10, 11, 12
	AD1PCFGbits.PCFG4 = 0; // Set AN as analog
	AD1CSSLbits.CSSL4 = 1; // AN as input channel for sequential reading
	TRISBbits.TRISB2 = 1; // Set RB as input
	AD1PCFGbits.PCFG5 = 0; // Set AN as analog
	AD1CSSLbits.CSSL5 = 1; // AN as input channel for sequential reading
	TRISBbits.TRISB3 = 1; // Set RB as input
	AD1PCFGbits.PCFG6 = 0; // Set AN as analog
	AD1CSSLbits.CSSL6 = 1; // AN as input channel for sequential reading
	TRISCbits.TRISC0 = 1; // Set RC as input
	AD1PCFGbits.PCFG7 = 0; // Set AN as analog
	AD1CSSLbits.CSSL7 = 1; // AN as input channel for sequential reading
	TRISCbits.TRISC1 = 1; // Set RC as input
	AD1PCFGbits.PCFG8 = 0; // Set AN as analog
	AD1CSSLbits.CSSL8 = 1; // AN as input channel for sequential reading
	TRISCbits.TRISC2 = 1; // Set RC as input
	AD1PCFGbits.PCFG9 = 0; // Set AN as analog
	AD1CSSLbits.CSSL9 = 1; // AN as input channel for sequential reading
	TRISBbits.TRISB15 = 1; // Set RB as input
	AD1PCFGbits.PCFG10 = 0; // Set AN as analog
	AD1CSSLbits.CSSL10 = 1; // AN as input channel for sequential reading
	TRISBbits.TRISB14 = 1; // Set RB as input
	AD1PCFGbits.PCFG11 = 0; // Set AN as analog
	AD1CSSLbits.CSSL11 = 1; // AN as input channel for sequential reading
	TRISBbits.TRISB13 = 1; // Set RB as input
	AD1PCFGbits.PCFG12 = 0; // Set AN as analog
	AD1CSSLbits.CSSL12 = 1; // AN as input channel for sequential reading
	TRISCbits.TRISC3 = 1; // Set RC as input

	AD1CON1bits.ADSIDL = 0; // Continue in Idle Mode
	AD1CON1bits.FORM = 0b00; // Integer Data Output
	AD1CON1bits.SSRC = 0b111; // Internal COunter for Trigger Source
	AD1CON1bits.ASAM = 1; // Sample Auto-Start

	AD1CON2bits.VCFG = 0b000; // Voltage Reference AVdd, AVss
	AD1CON2bits.CSCNA = 1; // CHannels specified by AD1CSSL register
	AD1CON2bits.SMPI = 0b1000; // Interrupt after completion of  8 sample(s)
	AD1CON2bits.BUFM = 0; // Buffer configured as 16-word
	AD1CON2bits.ALTS = 0; // Only use MUX A for sampling


	AD1CON3bits.ADRC = 0; // Conversion Clock from system clock
	AD1CON3bits.SAMC = 0b11111; // Auto-sample time bits 31 Tad
	AD1CON3bits.ADCS = 0b00000001; // Conversion CLock Period 2 * Tcy

	AD1CHSbits.CH0SA = 0b00000; // Positive input is AN0
	AD1CHSbits.CH0NA = 0; // Negative input is Vr-

	IFS0bits.AD1IF = 0; // Clear interrupt flag
	IEC0bits.AD1IE = 1; // Enable interrupt flag

	AD1CON1bits.ADON = 1;
	AD1CON1bits.SAMP = 1; // Start sampling
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