'''def add(*args):
    print args[0]
    return sum(args)

def colors(**kwargs):
    print kwargs.get('minHue')+5'''

if __name__ ==  '__main__':
    #print add(5,6,24,34)
    #colors(minHue = 5, b = 'dog', c = 'giraffe')
    import serial
    ser = serial.Serial(0)  # open first serial port
    print ser.portstr       # check which port was really used
    ser.write("hello")      # write a string
    ser.close()             # close port

