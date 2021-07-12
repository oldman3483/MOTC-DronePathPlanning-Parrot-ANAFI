# -*- coding: utf-8 -*-
"""
Created on Wed May 12 16:57:07 2021

@author: GPS
"""
import cv2
data = "../data/planpath_10buff_75m.png"
img = cv2.imread(data)



def OnMouseAction(event,x,y,flags,param):

    if event == cv2.EVENT_LBUTTONDOWN:
        print(str(x)+"   "+str(y))


cv2.namedWindow('image')
cv2.setMouseCallback('image',OnMouseAction)     
cv2.imshow('image',img)
cv2.waitKey(30000)
cv2.destroyAllWindows()