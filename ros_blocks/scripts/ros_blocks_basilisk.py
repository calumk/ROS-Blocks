#!/usr/bin/env python
import sys
import rospy
import cv
import cv2
import numpy as np
import baxter_interface
import baxter_external_devices
import os
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--w")
args = parser.parse_args()



path = os.path.dirname(os.path.realpath(__file__))

posx = 53                 # Define a point (posx, posy) on the source
posy = 153                  # image where the overlay will be placed 


class test_vision_node:

    def __init__(self):
        rospy.init_node('test_vision_node')

        """ Give the OpenCV display window a name. """
        self.cv_window_name = "OpenCV Image"

        """ Create the window and make it re-sizeable (second parameter = 0) """
        cv.NamedWindow(self.cv_window_name, 0)

        """ Create the cv_bridge object """
        self.bridge = CvBridge()

        """ Subscribe to the raw camera image topic """
        self.image_sub = rospy.Subscriber("/cameras/right_hand_camera/image", Image, self.callback)

    def callback(self, data):
        try:
            """ Convert the raw image to OpenCV format """
            cv_image = self.bridge.imgmsg_to_cv(data, "bgr8")
        except CvBridgeError, e:
          print e
        
        cv.Flip(cv_image,cv_image,-1)

        


        text_font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1)
        cv_imageDis = cv_image
        
        for i in range(16):
            cv.Line(cv_imageDis, (i*40,0), (i*40,400), cv.RGB(0, 168, 255), thickness=1, lineType=8, shift=0)
        for j in range(10):
            cv.Line(cv_imageDis, (0,j*40), (640,j*40), cv.RGB(0, 168, 255), thickness=1, lineType=8, shift=0)
            # Convert BGR to HSV
        cv_image = np.asarray(cv_image[:,:])
        cv_imageDis = np.asarray(cv_imageDis[:,:])
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        # define range of blue color in HSV
        lower_yellow = np.array([10, 60, 60])
        upper_yellow = np.array([30, 255, 255])
        
        lower_blue = np.array([100, 20, 10])
        upper_blue = np.array([120, 255, 255])

        lower_red = np.array([0, 21, 10])
        upper_red = np.array([5, 255, 255])

        lower_orange = np.array([5, 24, 13])
        upper_orange = np.array([13, 200, 200])

        lower_green = np.array([50, 21, 13])
        upper_green = np.array([76, 140, 100])


        # Threshold the HSV image to get only blue colors
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        # Bitwise-AND mask and original image
        #res = cv2.bitwise_and(cv_image,cv_image, mask= mask)
        kernel = np.ones((5,5),np.uint8)
        kernel2 = np.ones((20,20),np.uint8)

        erosion_yellow = cv2.erode(mask_yellow,kernel,iterations = 1)
        erosion_yellow = cv2.dilate(erosion_yellow,kernel,iterations = 1)

        erosion_blue = cv2.erode(mask_blue,kernel,iterations = 1)
        erosion_blue = cv2.dilate(erosion_blue,kernel,iterations = 1)
        
        erosion_red = cv2.erode(mask_red,kernel,iterations = 1)
        erosion_red = cv2.dilate(erosion_red,kernel,iterations = 1)
        
        erosion_orange = cv2.erode(mask_orange,kernel,iterations = 1)
        erosion_orange = cv2.dilate(erosion_orange,kernel2,iterations = 1)

        erosion_green = cv2.erode(mask_green,kernel,iterations = 1)
        erosion_green = cv2.dilate(erosion_green,kernel2,iterations = 1)

        
        cv2.imshow('erosion_yellow',erosion_yellow)
        cv2.imshow('erosion_blue',erosion_blue)
        cv2.imshow('erosion_red',erosion_red)
        cv2.imshow('erosion_orange',erosion_orange)
        cv2.imshow('erosion_green',erosion_green)
        cv2.imshow('frame',cv_imageDis)

        """OverlayImage(bgImage,cv_image,posx,posy)"""

        
        """ Refresh the image on the screen """
        """cv.ShowImage(self.cv_window_name, cv_image)"""
        cv.WaitKey(10)
        cv2.imwrite(path+'/ros_blocks_basilisk/out/color_yellow.png',erosion_yellow)
        cv2.imwrite(path+'/ros_blocks_basilisk/out/color_blue.png',erosion_blue)
        cv2.imwrite(path+'/ros_blocks_basilisk/out/color_red.png',erosion_red)
        cv2.imwrite(path+'/ros_blocks_basilisk/out/color_orange.png',erosion_orange)
        cv2.imwrite(path+'/ros_blocks_basilisk/out/color_green.png',erosion_green)

        if args.w:
            sys.exit()

def main(args):
      vn = test_vision_node()
      try:
        rospy.spin()
      except KeyboardInterrupt:
        print "Shutting down vison node."
      cv.DestroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)