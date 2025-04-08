/* 
 * File:   ryansheader.h
 * Author: Ryan
 *
 * Created on April 12, 2015, 1:16 PM
 */

#ifndef powermonitor_H
#define	powermonitor_H

/*
| I2C Address Assignment    | Value |   AD1    |   AD2    |
| :------------------------ | :---: | :------: | :------: |
| I2C_ADDRESS               | 0xCE  |   High   |   Low    |
| I2C_ADDRESS               | 0xD0  |   Float  |   High   |
| I2C_ADDRESS               | 0xD2  |   High   |   High   |
| I2C_ADDRESS               | 0xD4  |   Float  |   Float  |
| I2C_ADDRESS               | 0xD6  |   Float  |   Low    |
| I2C_ADDRESS               | 0xD8  |   Low    |   High   |
| I2C_ADDRESS               | 0xDA  |   High   |   Float  |
| I2C_ADDRESS               | 0xDC  |   Low    |   Float  |
| I2C_ADDRESS               | 0xDE  |   Low    |   Low    |
|                           |       |          |          |
| I2C_MASS_WRITE            | 0xCC  |    X     |    X     |
| I2C_ALERT_RESPONSE        | 0x19  |    X     |    X     |
*/

#define PM_1                       0xDE
#define PM_2                       0xD4

/******************  Registers  ***********************/
#define CTRLA_REG                           0x00
#define CTRLB_REG                           0x01
#define ALERT1_REG                          0x02
#define STATUS1_REG                         0x03
#define FAULT1_REG                          0x04
#define POWER_MSB2_REG                      0x05
#define POWER_MSB1_REG                      0x06
#define POWER_LSB_REG                       0x07
#define MAX_POWER_MSB2_REG                  0x08
#define MAX_POWER_MSB1_REG                  0x09
#define MAX_POWER_LSB_REG                   0x0A
#define MIN_POWER_MSB2_REG                  0x0B
#define MIN_POWER_MSB1_REG                  0x0C
#define MIN_POWER_LSB_REG                   0x0D
#define MAX_POWER_THRESHOLD_MSB2_REG        0x0E
#define MAX_POWER_THRESHOLD_MSB1_REG        0x0F
#define MAX_POWER_THRESHOLD_LSB_REG         0x10
#define MIN_POWER_THRESHOLD_MSB2_REG        0x11
#define MIN_POWER_THRESHOLD_MSB1_REG        0x12
#define MIN_POWER_THRESHOLD_LSB_REG         0x13
#define DELTA_SENSE_MSB_REG                 0x14
#define DELTA_SENSE_LSB_REG                 0x15
#define MAX_DELTA_SENSE_MSB_REG             0x16
#define MAX_DELTA_SENSE_LSB_REG             0x17
#define MIN_DELTA_SENSE_MSB_REG             0x18
#define MIN_DELTA_SENSE_LSB_REG             0x19
#define MAX_DELTA_SENSE_THRESHOLD_MSB_REG   0x1A
#define MAX_DELTA_SENSE_THRESHOLD_LSB_REG   0x1B
#define MIN_DELTA_SENSE_THRESHOLD_MSB_REG   0x1C
#define MIN_DELTA_SENSE_THRESHOLD_LSB_REG   0x1D
#define VIN_MSB_REG                         0x1E
#define VIN_LSB_REG                         0x1F
#define MAX_VIN_MSB_REG                     0x20
#define MAX_VIN_LSB_REG                     0x21
#define MIN_VIN_MSB_REG                     0x22
#define MIN_VIN_LSB_REG                     0x23
#define MAX_VIN_THRESHOLD_MSB_REG           0x24
#define MAX_VIN_THRESHOLD_LSB_REG           0x25
#define MIN_VIN_THRESHOLD_MSB_REG           0x26
#define MIN_VIN_THRESHOLD_LSB_REG           0x27
#define ADIN_MSB_REG                        0x28
#define ADIN_LSB_REG_REG                    0x29
#define MAX_ADIN_MSB_REG                    0x2A
#define MAX_ADIN_LSB_REG                    0x2B
#define MIN_ADIN_MSB_REG                    0x2C
#define MIN_ADIN_LSB_REG                    0x2D
#define MAX_ADIN_THRESHOLD_MSB_REG          0x2E
#define MAX_ADIN_THRESHOLD_LSB_REG          0x2F
#define MIN_ADIN_THRESHOLD_MSB_REG          0x30
#define MIN_ADIN_THRESHOLD_LSB_REG          0x31
#define ALERT2_REG                          0x32
#define GPIO_CFG_REG                        0x33
#define TIME_COUNTER_MSB3_REG               0x34
#define TIME_COUNTER_MSB2_REG               0x35
#define TIME_COUNTER_MSB1_REG               0x36
#define TIME_COUNTER_LSB_REG                0x37
#define CHARGE_MSB3_REG                     0x38
#define CHARGE_MSB2_REG                     0x39
#define CHARGE_MSB1_REG                     0x3A
#define CHARGE_LSB_REG                      0x3B
#define ENERGY_MSB3_REG                     0x3C
#define ENERGY_MSB2_REG                     0x3D
#define ENERGY_MSB1_REG                     0x3E
#define ENERGY_LSB_REG                      0x3F
#define STATUS2_REG                         0x40
#define FAULT2_REG                          0x41
#define GPIO3_CTRL_REG                      0x42
#define CLK_DIV_REG                         0x43


/****************  Command Codes  *********************/
#define ADIN_INTVCC                         0x80
#define ADIN_GND                            0x00
#define OFFSET_CAL_LAST                     0x60
#define OFFSET_CAL_128                      0x40
#define OFFSET_CAL_16                       0x20
#define OFFSET_CAL_EVERY                    0x00
#define CHANNEL_CONFIG_SNAPSHOT             0x07
#define CHANNEL_CONFIG_V_C                  0x06
#define CHANNEL_CONFIG_A_V_C_1              0x05
#define CHANNEL_CONFIG_A_V_C_2              0x04
#define CHANNEL_CONFIG_A_V_C_3              0x03
#define CHANNEL_CONFIG_V_C_1                0x02
#define CHANNEL_CONFIG_V_C_2                0x01
#define CHANNEL_CONFIG_V_C_3                0x00
#define ENABLE_ALERT_CLEAR                  0x80
#define ENABLE_SHUTDOWN                     0x40
#define ENABLE_CLEARED_ON_READ              0x20
#define ENABLE_STUCK_BUS_RECOVER            0x10
#define DISABLE_ALERT_CLEAR                 0x7F
#define DISABLE_SHUTDOWN                    0xBF
#define DISABLE_CLEARED_ON_READ             0xDF
#define DISABLE_STUCK_BUS_RECOVER           0xEF
#define ACC_PIN_CONTROL                     0x08
#define DISABLE_ACC                         0x04
#define ENABLE_ACC                          0x00
#define RESET_ALL                           0x03
#define RESET_ACC                           0x02
#define ENABLE_AUTO_RESET                   0x01
#define DISABLE_AUTO_RESET                  0x00
#define MAX_POWER_MSB2_RESET                0x00
#define MIN_POWER_MSB2_RESET                0xFF
#define MAX_DELTA_SENSE_MSB_RESET           0x00
#define MIN_DELTA_SENSE_MSB_RESET           0xFF
#define MAX_VIN_MSB_RESET                   0x00
#define MIN_VIN_MSB_RESET                   0xFF
#define MAX_ADIN_MSB_RESET                  0x00
#define MIN_ADIN_MSB_RESET                  0xFF
#define ENABLE_MAX_POWER_ALERT              0x80
#define ENABLE_MIN_POWER_ALERT              0x40
#define DISABLE_MAX_POWER_ALERT             0x7F
#define DISABLE_MIN_POWER_ALERT             0xBF
#define ENABLE_MAX_I_SENSE_ALERT            0x20
#define ENABLE_MIN_I_SENSE_ALERT            0x10
#define DISABLE_MAX_I_SENSE_ALERT           0xDF
#define DISABLE_MIN_I_SENSE_ALERT           0xEF
#define ENABLE_MAX_VIN_ALERT                0x08
#define ENABLE_MIN_VIN_ALERT                0x04
#define DISABLE_MAX_VIN_ALERT               0xF7
#define DISABLE_MIN_VIN_ALERT               0xFB
#define ENABLE_MAX_ADIN_ALERT               0x02
#define ENABLE_MIN_ADIN_ALERT               0x01
#define DISABLE_MAX_ADIN_ALERT              0xFD
#define DISABLE_MIN_ADIN_ALERT              0xFE
#define ENABLE_ADC_DONE_ALERT               0x80
#define DISABLE_ADC_DONE_ALERT              0x7F
#define ENABLE_GPIO_1_ALERT                 0x40
#define DISABLE_GPIO_1_ALERT                0xBF
#define ENABLE_GPIO_2_ALERT                 0x20
#define DISABLE_GPIO_2_ALERT                0xDF
#define ENABLE_STUCK_BUS_WAKE_ALERT         0x08
#define DISABLE_STUCK_BUS_WAKE_ALERT        0xF7
#define ENABLE_ENERGY_OVERFLOW_ALERT        0x04
#define DISABLE_ENERGY_OVERFLOW_ALERT       0xFB
#define ENABLE_CHARGE_OVERFLOW_ALERT        0x02
#define DISABLE_CHARGE_OVERFLOW_ALERT       0xFD
#define ENABLE_COUNTER_OVERFLOW_ALERT       0x01
#define DISABLE_COUNTER_OVERFLOW_ALERT      0xFE

#define GPIO1_IN_ACTIVE_HIGH                0xC0
#define GPIO1_IN_ACTIVE_LOW                 0x80
#define GPIO1_OUT_HIGH_Z                    0x40
#define GPIO1_OUT_LOW                       0x00

#define GPIO2_IN_ACTIVE_HIGH                0x30
#define GPIO2_IN_ACTIVE_LOW                 0x20
#define GPIO2_OUT_HIGH_Z                    0x10
#define GPIO2_OUT_LOW                       0x12
#define GPIO2_IN_ACC                        0x00

#define GPIO3_IN_ACTIVE_HIGH                0x0C
#define GPIO3_IN_ACTIVE_LOW                 0x08
#define GPIO3_OUT_REG_42                    0x04
#define GPIO3_OUT_ALERT                     0x00
#define GPIO3_OUT_LOW                       0x40
#define GPIO3_OUT_HIGH_Z                    0x00
#define GPIO_ALERT_CLEAR                    0x00


/******* Voltage Selection Command *******/
#define DELTA_SENSE                         0x00
#define VDD                                 0x08
#define ADIN                                0x10
#define SENSE_PLUS                          0x18


/*********** Register Mask Command ***************/
#define CTRLA_ADIN_MASK                     0x7F
#define CTRLA_OFFSET_MASK                   0x9F
#define CTRLA_VOLTAGE_SEL_MASK              0xE7
#define CTRLA_CHANNEL_CONFIG_MASK           0xF8
#define CTRLB_ACC_MASK                      0xF3
#define CTRLB_RESET_MASK                    0xFC
#define GPIOCFG_GPIO1_MASK                  0x3F
#define GPIOCFG_GPIO2_MASK                  0xCF
#define GPIOCFG_GPIO3_MASK                  0xF3
#define GPIOCFG_GPIO2_OUT_MASK              0xFD
#define GPIO3_CTRL_GPIO3_MASK               0xBF


/***************** Function Prototypes *****************/
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


// Clears all thresholds in the power monitor
void clearPMRegisters(char addr)
{
    I2Cwrite(addr, CTRLB_REG, RESET_ALL);
}


// Calculate and return the VIN voltage in Volts
// ADC value, VIN(lsb)
float voltage(int16_t adc_code, float weight)
{
    float voltage;
    voltage = (float)adc_code*weight;
    return(voltage);
}


// Calculate and return the current in Amps
// ADC value, the resistor value, delta sense(lsb)
float current(int16_t adc_code, float resistor, float weight)
{
    float voltage, current;
    voltage = (float)adc_code*weight;
    current = voltage/resistor;
    return(current);
}


// Calculate and return the power in Watts
// ADC value, the resistor value, power(lsb)
float power(int32_t adc_code, float resistor, float Power_lsb);



// Calculate and return the energy in Joules
// ADC value, resistor value, power(lsb), time(lsb)
float energy(int32_t adc_code, float resistor, float Power_lsb, float TIME_lsb);



// Calculate and return the charge in Coulombs
// ADC value, resistor value, delta sense(lsb), time(lsb)
float coulombs(int32_t adc_code, float resistor, float DELTA_SENSE_lsb, float Time_lsb);



// Calculate and return the internal time base in seconds
// time adc code, time(lsb)
float time(float time_code, float Time_lsb);



#endif	/* powermonitor_H */

