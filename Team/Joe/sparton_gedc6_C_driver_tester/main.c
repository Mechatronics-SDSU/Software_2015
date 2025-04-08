/* 
 * File:   main.c
 * Author: Joe
 * Purpose: To test the GEDC-6 driver files
 * Created on September 26, 2014, 9:09 PM
 */

#include <stdio.h>
#include <stdlib.h>
#include <arpa/inet.h>

#include "sparton_gedc6_interface.h"
#include "sparton_rfs_driver.h"

#define ARR_SIZE 256
#define COM_PORT 6
#define ITERATIONS 2000 // This is the number of stream data elements to process
#define NUM_VARIABLES 14
#define TIME_PERIOD 20
#define VARIABLES_OFFSET 13

/* Local Variables */
FILE * outputFD;

/*
 * 
 */
int main(int argc, char** argv) {
    
    int FD; /* File descriptor for the COM port */
    int n; /* Generic iterator */
    int i; /* Generic iterator */
    int idx = 0;
    unsigned char cmd_buff[ARR_SIZE];
    unsigned char crc_cmd_buff[ARR_SIZE];
    
    /* Set the stream mode in the Sparton AHRS */
    unsigned char rate[20] = "positionrate 20 set\0";
    unsigned char stop_rate[19] = "positionrate 0 set\0";
    
    unsigned char arrBuffer[ARR_SIZE];
    int msgChar = 0;
    
    int tmpCounter;
    
    float * myflt; // Float used to convert the values from the AHRS
    float flt;
    unsigned int myint;    
    unsigned int * pmyint;
    
    volatile int k; /* Generic iterator */
    
    int ret_bytes = 0; /* count of bytes returned */
    unsigned char ret[ARR_SIZE]; /* data buffer of returned bytes */
    
    unsigned char * data;
    
    FD = open_port(COM_PORT);
    printf("open_port = %i\n", FD);  
    
    /* Open the output data file */
    outputFD = fopen("output.txt", "w");
    if(outputFD == NULL){
        printf("ERROR!!!");
        exit(1);
    }    
    
    // Set all the bytes in the array to default to zero
    for(n=0; n<ARR_SIZE; n++){ cmd_buff[n] = 0; crc_cmd_buff[n] = 0;}
    
    /* Write the stream mode to the AHRS */
    n = write(FD, rate, sizeof(rate));
    
    // Setup a packet to send to the unit
    /*
    cmd_buff[0] = SOH;// SOH - SAPP packet frame
    cmd_buff[1] = 0x0B;// SAPP packet body size
    cmd_buff[2] = 0x60;// Error Options - No Ack - RFS Protocol
    cmd_buff[3] = DLE;// DLE - 01 
    cmd_buff[4] = 0x81;// Revision Level (Show command is RFS1)
    cmd_buff[5] = 0x00;// payload size MSB
    cmd_buff[6] = 0x00;// payload size
    cmd_buff[7] = 0x00;// payload size
    cmd_buff[8] = 0x00;// payload size LSB
    cmd_buff[9] = CMD_GET_VALUE;// Show command
    cmd_buff[10] = 0x02; // Sequence number... using 2 so that we don't need a DLE byte
    cmd_buff[11] = 0x1E; // Variable for position
    
    cmd_buff[14] = ETX; 
    
    for(n=0; n<15; n++){
        printf("%02X ", cmd_buff[n]);
    }printf("\n");    
    
    tmpCounter = removeSOHFrame(crc_cmd_buff, cmd_buff, 15);
        
    for(n=0; n<tmpCounter; n++){
        printf("%02X ", crc_cmd_buff[n]);
    }printf("\n");    
    
    addCRC16(crc_cmd_buff+1, tmpCounter-3);
       
    for(n=0; n<tmpCounter; n++){
        printf("%02X ", crc_cmd_buff[n]);
    }printf("\n");     
    
    tmpCounter = addSOHFrame(cmd_buff, crc_cmd_buff, tmpCounter);
    
    for(n=2; n<tmpCounter; n++){
        printf("%02X ", cmd_buff[n]);
    }printf("\n");
            
    // Write a command to the device
    //n = write(FD, cmd_buff+2, tmpCounter-2);
    */

    printf("\n");
    printf("\n");
    
    /* Output a header for the file that we are going to output */
    fprintf(outputFD, "Time\tpitch\troll\tyawt\tmagErr\ttemperature\tmagp X\t"
            "magp Y\tmagp Z\taccelp X\taccelp Y\taccelp Z\tgyrop X\tgyrop Y\t"
            "gyrop Z\n");
    
    /* Loop forever to continuously collect data */
    while(1){//(ret_bytes <= 0){
       /* Attempt to read data from the interface */
       ret_bytes = read(FD, ret, ARR_SIZE);
       
       /* Check the returned number of bytes to verify we got something */
       if (ret_bytes > 0)
       {
           // Loop through all the bytes that were found on the interface
           for(k=0; k < ret_bytes; k++)
           {               
               // Fill a buffer with all the data in the buffer
               arrBuffer[msgChar++] = ret[k];
               
               // Check if the current char iteration is the end of transmission
               // And convert and then print the data to file
               if(msgChar > 1 && 
                  arrBuffer[msgChar-1] == ETX && 
                  arrBuffer[msgChar-2] != DLE) // This is needed to check for escape char
               {                   
                   // remove the soh frame
                   tmpCounter = removeSOHFrame(crc_cmd_buff, arrBuffer, msgChar-1);
                   
                   // Only get the variable data
                   data = crc_cmd_buff + VARIABLES_OFFSET;
                   tmpCounter -= VARIABLES_OFFSET;     
                   
                   // Get the data and say that it is an integer so we can 
                   // convert it to a IEEE float
                   pmyint = (unsigned int *)(data);

                   // Print the time interval to the file as the first field
                   fprintf(outputFD, "%i\t", idx*TIME_PERIOD);
                   idx++; // Update the index for times
                   
                   // Convert the data from byte to float and print to file
                   for(i=0; i<NUM_VARIABLES; i++)
                   {                       
                       myint = htonl(*(pmyint+i)); // Damn endianess
                       fprintf(outputFD,"%6.8f\t", *((float*)&myint));
                   }// END for                       
                           
                   // Make sure we add a newline after we output all the position data
                   fprintf(outputFD, "\n" ); 
                   
                   // Re-set the msgChar to 0 to count up again
                   msgChar = 0;
               }// END if(msgChar > 1 && arrBuffer[msgChar-1] == ETX && 
                //     arrBuffer[msgChar-2] != DLE)              
           } // END for(k=0; k < ret_bytes; k++)
       } // END if (ret_bytes > 0)
       
       // Exit condition to break out of the endless loop
       if(idx > ITERATIONS) break;
       
    }// END while(1){//(ret_bytes <= 0)  
    
    /* Stop the streaming of data */
    n = write(FD, stop_rate, sizeof(stop_rate));    
        
    /* Close down all of the opened file descriptors */
    close(FD); 
    
    /* Close the file we created */
    fclose(outputFD);
    
    printf("All Done!!!");

    return (EXIT_SUCCESS);
}

