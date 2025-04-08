import imp

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
        g.write(savedParameters)#writes parameters to the text file
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
        for arg in args:#adds any missing parameter
            if arg not in par.keys():
                par[arg] = 0
        for (k,v) in par.iteritems():#puts the parameters in a string
            try:
                int(v)
                savedParameters += '%s=%s\n' % (k,v)
            except ValueError:
                savedParameters += '%s=0\n' % (k)
                print('%s has an invalid value and has been set to 0' % (k))
        mymodule = imp.new_module('mymodule')#creates an empty module
        exec(savedParameters, mymodule.__dict__)#fills empty module with parameter values
        return mymodule 