
#include "sparton_gedc6_interface.h"

/*
  * 'open_port()' - Open serial port 1.
  *
  * Returns the file descriptor on success or -1 on error.
  */
 
int open_port(unsigned char port){
   
   int fd; /* File descriptor for the port */
  
   char comport[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
 
   memcpy(comport, COM_PORT_PREPEND, COM_PORT_PREPEND_SIZE);
   
   /* Specify which com port to use based on the passed parameter
    This needs to be an ASCII number
    */
   if (port <= 9){
       comport[COM_PORT_PREPEND_SIZE] = ASCII_ZERO + port - 1;
   }
   else if (port < 100){ /* Tens */
       comport[COM_PORT_PREPEND_SIZE] = ASCII_ZERO + port / 10;
       comport[COM_PORT_PREPEND_SIZE+1] =
           ASCII_ZERO + port - 1 - (port / 10) * 10;
   }
   else /* Hundreds */
   {
       comport[COM_PORT_PREPEND_SIZE] = ASCII_ZERO + port / 100;
       comport[COM_PORT_PREPEND_SIZE+1] =
           ASCII_ZERO + (port / 10) - (port / 100) * 10; 
       comport[COM_PORT_PREPEND_SIZE+2] =
           ASCII_ZERO + port - 1 - (port / 10) * 10;      
   }
  
   fd = open(comport, O_RDWR | O_NOCTTY | O_NDELAY);
   if (fd == -1){
    /* Could not open the port. */
     fprintf(stderr, "open_port: Unable to open %s - %s\n",
             comport, strerror(errno));
    #ifdef DEBUG
   }else{printf("open_port = %s\n", comport); 
    #endif
   }
 
   return (fd);
  
 }
