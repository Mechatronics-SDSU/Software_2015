'''
Created on Dec 25, 2014

@author: Jared
'''
import pygame, sys, os
from pygame.locals import *

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

class TextPrint:
    '''
    This class prints the joystick and button values to the robosub movement GUI as signed floating-point integers
    Only used for local joystick feedback in a pygame window.
    '''
    
    def __init__(self):
        '''
        Font initialization for *TextPrint* class.
        
        **Parameters**: \n
        * **No Input Parameters.**
        
        **Returns**: \n
        * **No Returns.**\n
        '''
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def my_print(self, screen, textString):
        '''
        Determines position in x/y coordinated of printed output
        
        **Parameters**: \n
        * **screen** - Object for output screen
        * **textString** - Output string
        
        **Returns**: \n
        * **No Return.**\n
        '''
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        '''
        Sets cursor to initial position
        
        **Parameters**: \n
        * **No Input Parameters.** 
        
        **Returns**: \n
        * **No Return.**\n
        '''
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        '''
        Indents cursor position (same effect as Tab)
        
        **Parameters**: \n
        * **No Input Parameters.** 
        
        **Returns**: \n
        * **No Return.**\n
        '''
        self.x += 10

    def unindent(self):
        '''
        Un-indents the cursor position (same effect as Shitf+Tab)
        
        **Parameters**: \n
        * **No Input Parameters.** 
        
        **Returns**: \n
        * **No Return.**\n
        '''
        self.x -= 10

class controller():
    def __init__(self, embed, window):
        self.screen = None
        self.window = window
        self.embed = embed
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        size = [800, 400]
        self.screen = pygame.display.set_mode(size)
        pygame.joystick.init()
        
    def setup(self):
        self.embed.update()
        pygame.font.init()
        #Loop until the user clicks the close button.
        done = False
        
        pygame.display.set_caption("Sub Controller")
        
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()
        
        # Initialize the joysticks
        #pygame.joystick.init()
        
        #while done==False:
        
    def run(self):
        # Get ready to print
        #pygame.joystick.init()
        pygame.font.init()
        textPrint = TextPrint()
        for x in range(1):
        
            for event in pygame.event.get(): # User did something
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: # If user clicked close
                        done=True # Flag that we are done so we exit this loop
        
                    # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
                    if event.type == pygame.JOYBUTTONDOWN:
                        print("Joystick button pressed.")
                    if event.type == pygame.JOYBUTTONUP:
                        print("Joystick button released.")
                    
                    
            # DRAWING STEP
            # First, clear the screen to white. Don't put other drawing commands
            # above this, or they will be erased with this command.
            self.screen.fill(WHITE)
            textPrint.reset()
        
            # Get count of joysticks
            joystick_count = pygame.joystick.get_count()
            #print "Number of joysticks: {}".format(joystick_count)
            textPrint.my_print(self.screen, "Number of joysticks: {}".format(joystick_count) )
            textPrint.indent()
            
            # assume first joystick
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            #print "Joystick {}".format(1)
            textPrint.my_print(self.screen, "Joystick {}".format(1) )
            textPrint.indent()
            
            # Get the name from the OS for the controller/joystick
            name = joystick.get_name()
            #print "Joystick name: {}".format(name)
            textPrint.my_print(self.screen, "Joystick name: {}".format(name))
            
            # Usually axis run in pairs, up/down for one, and left/right for the other
            axes = joystick.get_numaxes()
            #print "Number of axes: {}".format(axes)
            textPrint.my_print(self.screen, "Number of axes: {}".format(axes) )
            textPrint.indent()
            
            for i in range( axes ):
                axis = joystick.get_axis( i )
                #print "Axis {} value: {}".format(i, int(axis*100))
                if i == 1 or i == 3:
                    textPrint.my_print(self.screen, "Axis {} value: {:>6.3f}".format(i, (axis*-1)))
                else:
                    textPrint.my_print(self.screen, "Axis {} value: {:>6.3f}".format(i, (axis)))
            textPrint.unindent()
                
            buttons = joystick.get_numbuttons()
            #print "Number of buttons: {}".format(buttons)
            textPrint.my_print(self.screen, "Number of buttons: {}".format(buttons))
            textPrint.indent()
                
            for i in range( buttons ):
                    button = joystick.get_button( i )
                    if button == 1:
                        textPrint.my_print(self.screen, "Button {} value: True".format(i) )
                    else:
                        textPrint.my_print(self.screen, "Button {} value: False".format(i) )                
            textPrint.unindent()
            
            hats = joystick.get_numhats()
            #print "Number of hats: {}".format(hats)
            textPrint.my_print(self.screen, "Number of hats: {}".format(hats))
            
            for i in range( hats ):
                    hat = joystick.get_hat( i )
                    #print "Hat {} value: {}".format(i, str(hat))
                    textPrint.my_print(self.screen, "Hat {} value: {}".format(i, str(hat)))
            textPrint.unindent()
            
            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
                    
            '''axis0 = int(joystick.get_axis( 0 )*204)
            axis1 = int(joystick.get_axis( 1 )*204)
            axis2 = int(joystick.get_axis( 2 )*204)
            axis3 = int(joystick.get_axis( 3 )*204)
            axis4 = int(joystick.get_axis( 4 )*204)
            button0 = int(joystick.get_button( 0 ))
            button1 = int(joystick.get_button( 1 ))
            button2 = int(joystick.get_button( 2 ))
            button3 = int(joystick.get_button( 3 ))
            button4 = int(joystick.get_button( 4 ))
            button5 = int(joystick.get_button( 5 ))
            button6 = int(joystick.get_button( 6 ))
            button7 = int(joystick.get_button( 7 ))
            button8 = int(joystick.get_button( 8 ))
            button9 = int(joystick.get_button( 9 ))
            '''
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            #self.embed.update()
            
            # Limit to 20 frames per second
            #clock.tick(20)
            #pygame.quit()
            
            
        # Close the window and quit.
        # If you forget this line, the program will 'hang'
        # on exit if running from IDLE and using a local joystick.
        #pygame.quit ()
        
    def stop(self):
        pygame.init()
        pygame.quit()
