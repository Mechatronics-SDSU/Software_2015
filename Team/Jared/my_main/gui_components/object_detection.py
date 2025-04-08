'''
.. module:: object_detection
   :synopsis: Determines what qualifies as an object and tracks its coordinates.

:Author: Austin Owens <sdsumechatronics@gmail.com>
:Date: Created on Oct 21, 2013
:Description: This module stores the object detection classes. For more information on the object detection techniques being used, go to http://docs.opencv.org/2.4.5/modules/imgproc/doc/feature_detection.html?highlight=houghcircles#cv2.HoughCircles and http://docs.opencv.org/2.4.5/modules/video/doc/motion_analysis_and_object_tracking.html?highlight=camshift#cv2.CamShift

'''
import cv2
import my_main.utilities as utilities


refreshCamshift = utilities.Timer()
frontCamRetrackingTimer = utilities.Timer()
bottomCamRetrackingTimer = utilities.Timer()

class CircleDetect:
    '''
    This class is capable of finding circular objects. It is also possible to track objects of any shape by adjusting the parameters.
    This is because circular pixels are in every object. For example, by fine tuning the parameters, you can get this class to track the small
    circular pixels of a triangle or rectangle.
    '''
    def __init__(self, dp=2): #Inverse ratio of the accumulator resolution to the image resolution. For example, 
        '''
        Initializing values for *Circle_Detect*.
        
        **Parameters**: \n
        * **dp** - Inverse ratio of the accumulator resolution to the image resolution. For example, if dp=1 , the accumulator has the same resolution as the input image. If dp=2 , the accumulator has half as big width and height.
        
        **Returns**: \n
        * **No Return.**\n
        '''
        
        self.dp = dp

    def on(self, img, param1, param2, minDist, minRadius, maxRadius):
        '''
        Determines what qualifies as a trackable object.
        
        **Parameters**: \n
        * **img** - Image to have circle detect be performed upon.
        * **param1** - A threshold value. This value will vary depending upon what object you want to track.
        * **param2** - A threshold value. This value will vary depending upon what object you want to track.
        * **minDist** - Minimum distance between the centers of the detected circles.
        * **minRadius** - Minimum circle radius value.
        * **maxRadius** - Maximum circle radius value.
        
        **Returns**: \n
        * **circles** - Contains data about circles position and radius.\n
        '''
        
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, self.dp, minDist, 1, param1, param2, minRadius, maxRadius) #1 is a dummy value
        return circles

class Camshift:
    '''
    This class is capable of finding any object of any shape.
    '''
    def __init__(self):
        '''
        Initializing values for mouse events, counters, and camshift. \n
        
        **Parameters**: \n
        * **windowName** - The window name for camshift must be entered before using this class.
        
        **Returns**: \n
        * **No Return.**\n
        '''
        
        self.hist = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.track_window = (0, 0, 0, 0)
        self.track_box = ((0, 0), (0, 0), 0)
        self.retrackingTimer = 0.2 # Time in seconds from image lost to re-track
        self.firstOccurance = True
        self.showBackProjection = False
        self.refreshTime = 0
         
    def camshift(self, imgToWriteOn, hsv, mask, processedImgWidth, processedImgHeight):
        '''
        Determines what qualifies as a trackable object.
        
        **Parameters**: \n
        * **img** - Image to have camshift be performed upon.
        
        **Returns**: \n
        * **self.track_box** - Contains data about the objects position, size, and orientation.\n
        >>> ((X position, Y position), (ellipse width, ellipse height), (orientation)).
        '''
            
        if(self.firstOccurance): # initialize once only
            Camshift.__initilizeTrackingArea__(self, 0, 0, processedImgWidth, processedImgHeight, hsv, mask)
            self.firstOccurance = False
            
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
        prob = cv2.calcBackProject([hsv], [0], self.hist, [0, 180], 1)
        prob &= mask

        if self.track_window[2] > 0: #If camshift can detect something
            refreshTime = refreshCamshift.netTimer(refreshCamshift.cpuClockTimeInSeconds())
            if refreshTime >= self.refreshTime: #This allows tracking to refresh every 5 seconds so that it will always be tracking the most intense source
                refreshCamshift.restartTimer()
                Camshift.__initilizeTrackingArea__(self, 0, 0, processedImgWidth, processedImgHeight, hsv, mask)
            self.track_box, self.track_window = cv2.CamShift(prob, self.track_window, term_crit)
            
        else: #If camshift can not detect anything at all
            netTime = frontCamRetrackingTimer.netTimer(frontCamRetrackingTimer.cpuClockTimeInSeconds())
            if(netTime >= self.retrackingTimer):
                frontCamRetrackingTimer.restartTimer()
                Camshift.__initilizeTrackingArea__(self, 0, 0, processedImgWidth, processedImgHeight, hsv, mask)
                self.track_box, self.track_window = cv2.CamShift(prob, self.track_window, term_crit)
                
        try:
            cv2.ellipse(imgToWriteOn, self.track_box, (0, 0, 255), 2) # Makes the ellipse that is seen on the screen
        except:
            print "Ellipse function failed in ObjectDetection class"

        return self.track_box
    
    
    def __initilizeTrackingArea__(self, x, y, width, height, hsv, mask):
        '''
        A private function that finds the region of interest (ROI) through mouse events.
        
        **Parameters**: \n
        * **x** - X position of the top left point of the drag box for the ROI.
        * **y** - Y position of the top left point of the drag box for the ROI.
        * **width** - Width of the drag box for the ROI.
        * **height** - Height of the drag box for the ROI.
        * **hsv** - HSV for the ROI.
        * **mask** - Bitwise masking of the drag box for the ROI.
        
        **Returns**: \n
        * **No Return.**
        '''
        self.track_window = (x, y, width, height)
        hsv_roi = hsv[y:(height+y), x:(width+x)]
        mask_roi = mask[y:(height+y), x:(width+x)]
        self.hist = cv2.calcHist( [hsv_roi], [0], mask_roi, [16], [0, 180] )
        cv2.normalize(self.hist, self.hist, 0, 255, cv2.NORM_MINMAX)
        self.hist = self.hist.reshape(-1)