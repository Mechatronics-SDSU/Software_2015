import imp
from random import randint
import time
import collections
start_time = time.clock()

class Log():
    '''
    This class saves and reads in parameter values from a text file. If the text file is blank upon reading in values, 
    this class will create those values and fill them in with ones.
    '''
    def __init__(self, fileName):
        self.fileName = fileName 
        '''
        Sets the filename
        **Parameters**: \n
        * **fileName** - The location name of the file to read the saved parameters from.
        
        **Returns**: \n
        * **No Return.**\n
        '''
        
    def writeParameters(self, **kwargs):#writes the last values recorded for the parameters in a text file
        '''
        Writes the values for specified parameters specified in kwargs in a text file 
        **Parameters**: \n
        * ***kwargs** - Parameters with their values, written as parameter=value; to request more than one, separate the component ID's by commas.
        
        **Returns**: \n
        * **No Return.**\n
        '''
        savedParameters = ''
        par = {}
        try:
            f = open(self.fileName, 'r')
        except:
            with open(self.fileName, 'w') as f:
                f.write('')
            f = open(self.fileName, 'r')
        if (len(f.readlines()) > 0):#if there is something in the file, write to it
            f.seek(0)#puts pointer at beginning of file since f.read made pointer go to the end of the file
            values = f.readlines()
            
            for line in values:#passes over the old parameters
                if line.strip() != '':
                    key, value = line.split("=")
                    par[key] = value.strip()
                    
        par.update(kwargs)#updates the new parameters
        for (k,v) in par.iteritems():
            savedParameters += '%s=%s\n' % (k,v)
        f.close()
        g = open(self.fileName, 'w')
        g.write(savedParameters)
        g.close()

    def getParameters(self, *args):
        '''
        Reads in the specified parameter values by using a dictionary 
        You can call each one using object.parametername  
        **Parameters**: \n
        * **args** - Any number of parameters are read as strings, separated by a comma
        
        **Returns**: \n
        * **mymodule** - module containing values of the specified parameters
        '''
        savedParameters = ''
        par = {}
        try:
            f = open(self.fileName, 'r')
        except:
            with open(self.fileName, 'w') as f:
                f.write('')
            f = open(self.fileName, 'r')
        if (len(f.readlines()) > 0):#if there is something in the file, read the params and return them
            f.seek(0)
            values = f.readlines()
            
            for line in values:#writes new value for parameter
                if line.strip() != '':
                    key, value = line.split("=")
                    if key in args:#writes the value of the parameter
                        par[key] = value.strip()
        for arg in args:
            if arg not in par.keys():
                par[arg] = 0
        for (k,v) in par.iteritems():
            try:
                int(v)
                savedParameters += '%s=%s\n' % (k,v)
            except ValueError:
                savedParameters += '%s=0\n' % (k)
                print('%s has an invalid value and has been set to 0' % (k))
        mymodule = imp.new_module('mymodule')
        exec(savedParameters, mymodule.__dict__)
        return mymodule            
                    
if __name__ == '__main__':
    
    logger = Log("Parameters.txt") #Making an instance of class 'Log'
    
    Flag = 0

    if Flag == 0:
        p = Log("Parameters.txt").getParameters('minHue', 'maxHue', 'minVal', 'm')
        logger.writeParameters(minHue = p.minHue, maxHue = p.maxHue, m=.545156146, n=45, z=4)    
        minHue = p.minHue#brings in the parameters to be used
        maxHue = p.maxHue
        minVal = p.minVal
        print 'minHue=' + str(minHue)
        print 'maxHue=' + str(maxHue)
        print 'minVal=' + str(minVal)
        #Flag = 1
        
    if Flag == 1:#write
        maxHue = randint(0,255)#simulating changing the values
        maxSat = randint(0,255)
        maxVal = randint(0,255)
        minSat = randint(0,255)
        minVal = randint(0,255)
        minHue = randint(0,255)
        logger.writeParameters(minHue = minHue, maxHue = maxHue, minSat = minSat)
        logger.writeParameters(maxSat = maxSat, minVal = minVal, maxVal = maxVal)
        print 'minHue=' + str(minHue)
        print 'maxHue=' + str(maxHue)
        print 'minSat=' + str(minSat)
        print 'maxSat=' + str(maxSat)
        print 'minVal=' + str(minVal)
        print 'maxVal=' + str(maxVal)
        
    if Flag == 2:
        for x in range(0, 1):
            maxHue = randint(0,255)#simulating changing the values
            maxSat = randint(0,255)
            maxVal = randint(0,255)
            minSat = randint(0,255)
            minVal = randint(0,255)
            minHue = randint(0,255)
            
            hsvVals = logger.getParameters('minHue', 'maxHue', 'minVal')  
            print hsvVals.minHue, hsvVals.maxHue, hsvVals.minVal
            logger.writeParameters(minHue = minHue, maxHue = maxHue, minSat = minSat, m=1, n=3, z=4)
            
            newValues = logger.getParameters('newVal')
            print newValues.newVal
            logger.writeParameters(newVal = 20)
            
            moreValues = logger.getParameters('morVal')
            print moreValues.morVal
print("--- %s seconds ---" % str(time.clock() - start_time))