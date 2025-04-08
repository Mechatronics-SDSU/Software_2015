/* 
 * File:   sparton_gedc6_interface.h
 * Author: Joe
 *
 * Created on September 28, 2014, 8:42 PM
 */

#ifndef SPARTON_GEDC6_INTERFACE_H
#define	SPARTON_GEDC6_INTERFACE_H

#ifdef	__cplusplus
extern "C" {
#endif
    
#include <stdio.h> /* Standard input/output definitions */
#include <stdlib.h>
#include <string.h>  /* String function definitions */
#include <unistd.h>  /* UNIX standard function definitions */
#include <fcntl.h>   /* File control definitions */
#include <errno.h>   /* Error number definitions */
#include <termios.h> /* POSIX terminal control definitions */    

/* Define this for debug mode */
#define DEBUG
 
/* Prepended string that defines the COM port interface */
#define COM_PORT_PREPEND ("/dev/ttyS")
#define COM_PORT_PREPEND_SIZE (9)

/* Baud Rates */
#define BAUD_57600 (2)
 
/* ASCII Character for ZERO */
#define ASCII_ZERO (48)
    
/* Function prototypes */
int open_port(unsigned char port);


#ifdef	__cplusplus
}
#endif

#endif	/* SPARTON_GEDC6_INTERFACE_H */

