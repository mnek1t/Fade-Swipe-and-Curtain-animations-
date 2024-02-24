import cv2                              # OpenCV for working with images
import numpy as np                      # for working with arrays and making math with it
import time                             # for providing time-related functions
import copy                             # for making a copy of variables
from matplotlib import pyplot as plt    # for creating static, animated, and interactive visualizations
import PySimpleGUI as sg                # for making graphical user interface
""" import locale
locale.setlocale(locale.LC_ALL, 'Russian') """

#create Text and Input fields + button with browsing files from computer drive + button Start and Close
layout = [
    [sg.Text('File 1'), sg.InputText(),sg.FileBrowse(),],  
    [sg.Text('File 2'), sg.InputText(), sg.FileBrowse(),],
    [sg.Submit('Start'), sg.Cancel('Close')]
]
# create the Window
window = sg.Window('Image processor', layout) 
#The Event LOOP
while True:
    #read information from user`s input
    event, values = window.read()
    
    if event in (None, 'Exit', 'Close'):
        break
    
    #read the absolute path of image
    img1 = cv2.imread(str(values[0]), 1) 
    img2 = cv2.imread(str(values[1]), 1)
    
    # convert image to RGB because of properties of OpenCV library
    #im_rgb1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    #im_rgb2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    
    #resize images to one size
    resized_img_1 = cv2.resize(img1, (200,200))
    resized_img_2 = cv2.resize(img2, (200,200))
    
    #take exact height and width of images
    resized_img_1_height = resized_img_1.shape[0]
    resized_img_1_width = resized_img_1.shape[1]
    resized_img_2_height = resized_img_2.shape[0]
    resized_img_2_width = resized_img_2.shape[1]

    #creating animation: FADE
    for i in np.linspace (0,1,100):
        #The alpha and beta variables are the constant or weight for the first and second image respectively
        alpha = i 
        beta = 1-alpha
        #output = cv2.addWeighted(resized_img_2,alpha,resized_img_1,beta,0)      #realize transition effect
        output = np.uint8(alpha * (resized_img_2)  + beta * (resized_img_1)+ 0)
        result = np.concatenate((resized_img_1, resized_img_2, output), axis=1)# concatenate image Horizontally
        cv2.imshow("Output result", result) #display images in a window
        time.sleep (0.02) #suspend execution for the given number of seconds
        if (cv2.waitKey(1) == 27): #allows users to display a window for given milliseconds or until any key is pressed
            break 
    
    #creating animation Swipe (from top to bottom)
    time.sleep (1)
    output= copy.copy(resized_img_1) #make a copy of image 1
    for j in range(resized_img_1_width): #iterator j is responsible for rows
        for i in range(resized_img_1_height):#iterator i is responsible for columns
            output[j, i] = resized_img_2[j, i] #replace given pixel by another one
        result = np.concatenate((resized_img_1, resized_img_2, output), axis=1)
        cv2.imshow("Output result", result)
        time.sleep (0.02)
        if (cv2.waitKey(1) == 27):
            break
    
    #creating animation: Curtain
    output= copy.copy(resized_img_1)
    #addition variables for moving left and right from the middle of the image       
    left=int(resized_img_1_height/2)
    right=int(resized_img_1_height/2)-1
    time.sleep (1)
    for j in range(int(resized_img_1_width/2)+1): # iterator j is responsible for columns
        #for each iteration move on one pixel left and right accordingly
        left = left-1
        right = right+1
        #exception to avoid being out of array
        if(left<0 or right>resized_img_1_width):
            break
        for i in range(resized_img_1_height): # iterator i is responsible for rows
            output[i, left] = resized_img_2[i, left]
            output[i, right] = resized_img_2[i, right]
        result = np.concatenate((resized_img_1, resized_img_2, output), axis=1)
        cv2.imshow("Output result", result)
        time.sleep (0.02)
        if (cv2.waitKey(1) == 27):
            break

cv2.destroyAllWindows() #destroy all the windows we created