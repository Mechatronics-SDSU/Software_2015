/* 
 * File:   austins_PIC24FJ32GB002_lib.h
 * Author: Austin
 *
 * Created on January 31, 2015, 12:18 AM
 */

#ifndef AUSTINS_PIC24FJ32GB002_LIB_H
#define AUSTINS_PIC24FJ32GB002_LIB_H

/*
REGISTER NUMBERS ON PIC24J32GB002 (USED FOR TRIS REGISTER)
+------+---------+------+---------+
| PINS | REG NUM | PINS | REG NUM |
+------+---------+------+---------+
|   1  |  *NONE* |  15  |  *NONE* |
|   2  |    RA0  |  16  |    RB7  |
|   3  |    RA1  |  17  |    RB8  |
|   4  |    RB0  |  18  |    RB9  |
|   5  |    RB1  |  19  |  *NONE* |
|   6  |    RB2  |  20  |  *NONE* |
|   7  |    RB3  |  21  |   RB10  |
|   8  |  *NONE* |  22  |   RB11  |
|   9  |    RA2  |  23  |  *NONE* |
|  10  |    RA3  |  24  |   RB13  |
|  11  |    RB4  |  25  |   RB14  |
|  12  |    RA4  |  26  |   RB15  |
|  13  |  *NONE* |  27  |  *NONE* |
|  14  |    RB5  |  28  |  *NONE* |
+------+---------+------+---------+
*/

//INPUT/OUTPUT
#define INPUT  1
#define OUTPUT 0

//ON/OFF
#define ON  1
#define OFF 0

//PIN NUMBER TO TRI STATE REGISTER (TRIS) (EX: PIN26_TRIS = OUTPUT)
#define PIN2_TRIS  TRISAbits.TRISA0
#define PIN3_TRIS  TRISAbits.TRISA1
#define PIN4_TRIS  TRISBbits.TRISB0
#define PIN5_TRIS  TRISBbits.TRISB1
#define PIN6_TRIS  TRISBbits.TRISB2
#define PIN7_TRIS  TRISBbits.TRISB3
#define PIN9_TRIS  TRISAbits.TRISA2
#define PIN10_TRIS TRISAbits.TRISA3
#define PIN11_TRIS TRISBbits.TRISB4
#define PIN12_TRIS TRISAbits.TRISA4
#define PIN14_TRIS TRISBbits.TRISB5
#define PIN16_TRIS TRISBbits.TRISB7
#define PIN17_TRIS TRISBbits.TRISB8
#define PIN18_TRIS TRISBbits.TRISB9
#define PIN21_TRIS TRISBbits.TRISB10
#define PIN22_TRIS TRISBbits.TRISB11
#define PIN24_TRIS TRISBbits.TRISB13
#define PIN25_TRIS TRISBbits.TRISB14
#define PIN26_TRIS TRISBbits.TRISB15

//PIN NUMBER TO LATCH REGISTER (LAT) (EX: PIN2_LAT = ON)
#define PIN2_LAT  LATAbits.LATA0
#define PIN3_LAT  LATAbits.LATA1
#define PIN4_LAT  LATBbits.LATB0
#define PIN5_LAT  LATBbits.LATB1
#define PIN6_LAT  LATBbits.LATB2
#define PIN7_LAT  LATBbits.LATB3
#define PIN9_LAT  LATAbits.LATA2
#define PIN10_LAT LATAbits.LATA3
#define PIN11_LAT LATBbits.LATB4
#define PIN12_LAT LATAbits.LATA4
#define PIN14_LAT LATBbits.LATB5
#define PIN16_LAT LATBbits.LATB7
#define PIN17_LAT LATBbits.LATB8
#define PIN18_LAT LATBbits.LATB9
#define PIN21_LAT LATBbits.LATB10
#define PIN22_LAT LATBbits.LATB11
#define PIN24_LAT LATBbits.LATB13
#define PIN25_LAT LATBbits.LATB14
#define PIN26_LAT LATBbits.LATB15

//PIN NUMBER TO ANALOG REGISTER (AN) (EX: AD1CHSbits.CH0SA = PIN24_AN)
#define PIN2_AN   0
#define PIN3_AN   1
#define PIN4_AN   2
#define PIN5_AN   3
#define PIN6_AN   4
#define PIN7_AN   5
#define PIN24_AN 11
#define PIN25_AN 10
#define PIN26_AN  9

//PIN NUMBER TO REMAPPABLE PIN REGISTER (RP) FOR INPUT (EX: INT1_I = PIN2_RPI)
#define PIN2_RPI   5
#define PIN3_RPI   6
#define PIN4_RPI   0
#define PIN5_RPI   1
#define PIN6_RPI   2
#define PIN7_RPI   3
#define PIN11_RPI  4
#define PIN16_RPI  7
#define PIN17_RPI  8
#define PIN18_RPI  9
#define PIN21_RPI 10
#define PIN22_RPI 11
#define PIN24_RPI 13
#define PIN25_RPI 14
#define PIN26_RPI 15

//REMAPPABLE PIN INPUT REGISTER FUNCTIONS (RPIR) (EX: INT1_I = PIN2_RPI)
#define INT1_I   RPINR0bits.INT1R
#define INT2_I   RPINR1bits.INT2R
#define IC1_I    RPINR7bits.IC1R
#define IC2_I    RPINR7bits.IC2R
#define IC3_I    RPINR8bits.IC3R
#define IC4_I    RPINR8bits.IC4R
#define IC5_I    RPINR9bits.IC5R
#define OCFA_I   RPINR11bits.OCFAR
#define OCFB_I   RPINR11bits.OCFBR
#define SCK1IN_I RPINR20bits.SCK1R
#define SDI1_I   RPINR20bits.SDI1R
#define SS1IN_I  RPINR21bits.SS1R
#define SCK2IN_I RPINR22bits.SCK2R
#define SDI2_I   RPINR22bits.SDI2R
#define SS2IN_I  RPINR23bits.SS2R
#define T2CK_I   RPINR3bits.T2CKR
#define T3CK_I   RPINR3bits.T3CKR
#define T4CK_I   RPINR4bits.T4CKR
#define T5CK_I   RPINR4bits.T5CKR
#define U1CTS_I  RPINR18bits.U1CTSR
#define U1RX_I   RPINR18bits.U1RXR
#define U2CTS_I  RPINR19bits.U2CTSR
#define U2RX_I   RPINR19bits.U2RXR

//PIN NUMBER TO REMAPPABLE PIN REGISTER (RP) FOR OUTPUT (EX: PIN5_RPO = OC_5)
#define PIN2_RPO  RPOR2bits.RP5R
#define PIN3_RPO  RPOR3bits.RP6R
#define PIN4_RPO  RPOR0bits.RP0R
#define PIN5_RPO  RPOR0bits.RP1R
#define PIN6_RPO  RPOR1bits.RP2R
#define PIN7_RPO  RPOR1bits.RP3R
#define PIN11_RPO RPOR2bits.RP4R
#define PIN16_RPO RPOR3bits.RP7R
#define PIN17_RPO RPOR4bits.RP8R
#define PIN18_RPO RPOR4bits.RP9R
#define PIN21_RPO RPOR5bits.RP10R
#define PIN22_RPO RPOR5bits.RP11R
#define PIN24_RPO RPOR6bits.RP13R
#define PIN25_RPO RPOR7bits.RP14R
#define PIN26_RPO RPOR7bits.RP15R

//REMAPPABLE PIN OUTPUT REGISTER FUNCTIONS (RPOR) (EX: PIN5_RPO = OC_5)
#define NULL_O     0
#define C1OUT_O    1
#define C2OUT_O    2
#define U1TX_O     3
#define U1RTS_O    4
#define U2TX_O     5
#define U2RTS_O    6
#define SDO1_O     7
#define SCK1OUT_O  8
#define SS1OUT_O   9
#define SDO2_O    10
#define SCK2OUT_O 11
#define SS2OUT_O  12
#define OC1_O     18
#define OC2_O     19
#define OC3_O     20
#define OC4_O     21
#define OC5_O     22
#define CTPLS_O   29
#define C3OUT_O   30

//OUTPUT COMPARE TIMER SELECT (OCTSEL)
#define SYSTEM_CLOCK 0b111
#define TIMER1       0b100
#define TIMER2       0b000
#define TIMER3       0b001
#define TIMER4       0b010
#define TIMER5       0b011

//OUTPUT COMPARE MODE
#define CENTER_ALIGNED_PWM                  0b111
#define EDGE_ALIGNED_PWM                    0b110
#define DOUBLE_COMPARE_CONTINUOUS_PULSE     0b101
#define DOUBLE_COMPARE_SINGLE_SHOT          0b100
#define SINGLE_COMPARE_CONTINUOUS_PULSE     0b011
#define SINGLE_COMPARE_SINGLE_SHOT_HIGH_LOW 0b010
#define SINGLE_COMPARE_SINGLE_SHOT_LOW_HIGH 0b001
#define OUTPUT_COMAPRE_DISABLE              0b000


#endif

