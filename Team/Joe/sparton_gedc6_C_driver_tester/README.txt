This project was developed using NetBeans 8.0.1 and the Cygwin tool chain 
which should enable this to compile in the Linux environment as well.

You will have to change the COM port using the define statements in the main
file. This could work with Windows but the method of opening a COM port is
different.  This code a little raw because it is not meant for production
and will not be used in the robo sub.

The ouptut of running this goes to a tab delimited file called 'output.txt'
which contains the position variable decomposed from the raw RFS protcol 
into readable floats.  This will enable the use of Excel to process the
data by hand.