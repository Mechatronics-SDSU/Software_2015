/* 
 * File:   sparton_rfs_driver.h
 * Author: Joe
 *
 * Created on September 26, 2014, 9:25 PM
 */

#ifndef SPARTON_RFS_DRIVER_H
#define	SPARTON_RFS_DRIVER_H

#ifdef	__cplusplus
extern "C" {
#endif

/* Include files */    
#include "sparton_gedc6_interface.h"    

/* Macro Define Statements */
/* DLE need for DLE, SOH, SYN, ACK, NAK, ETX */    
#define NOMINAL_CRC_SEED 0xFFFF
#define NUL 0x00 /* null */
#define SOH 0x01 /* start of header */
#define STX 0X02 /* start of text */
#define ETX 0x03 /* end of text */
#define EOT 0x04 /* end of transmission */
#define ENQ 0x05 /* enquiry */
#define ACK 0x06 /* acknowledge */
#define BEL 0x07 /* bell or alarm */
#define BS 0x08 /* backspace */
#define HT 0x09 /* horizontal tab */
#define LF 0x0A /* line feed */
#define VT 0x0B /* vertical tab */
#define FF 0x0C /* form feed */
#define CR 0x0D /* carriage return */
#define SO 0x0E /* shift out */
#define SI 0x0F /* shift in */
#define DLE 0x10 /* data link escape */
#define DC1 0x11 /* device control 1 CTRL_Q */
#define DC2 0x12 /* device control 2 */
#define DC3 0x13 /* device control 3 CTRL_S */
#define DC4 0x14 /* device control 4 */
#define NAK 0x15 /* negative acknowledge */
#define SYN 0x16 /* synchronous idle */

#define MASK_UP 0x80
#define MASK_OFF 0x7f
    
/* Command codes */
#define CMD_GET_RESPONSE 0
#define CMD_GET 1
#define CMD_GET_NEXT 2
#define CMD_SET 3
#define CMD_TRAP 4
#define CMD_SHOW 5
#define CMD_FORMAT 6
#define CMD_GET_PREV 7
#define CMD_GET_VALUE 8
#define CMD_VALUE_IS 9
#define CMD_GET_NEXT_VALUE 10
#define CMD_GET_PREVIOUS_VALUE 11
#define CMD_CONSTRUCT 12
#define CMD_ERROR 127
    

/* Custom data types */
typedef unsigned char Byte;
typedef unsigned short int Word16;
typedef unsigned int Word32;
typedef short int Int16;
typedef int Int43;

typedef struct{
    Byte byteCount;
    Byte error;
    Byte protocol;
    Byte protocol_version;
    Word32 payload_size;
    Byte command;
    Byte sequence_id;
    Byte vid1;
    Byte vid2;
    Byte payload[1024];
    Word16 crc;    
}t_rfs_packet;

/* Global function prototypes */




#ifdef	__cplusplus
}
#endif

#endif	/* SPARTON_RFS_DRIVER_H */

