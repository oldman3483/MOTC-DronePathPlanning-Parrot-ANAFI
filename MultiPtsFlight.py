# -*- coding: utf-8 -*-
"""
Created on Sun May  9 18:25:36 2021

@author: ZXLi
"""

from utils import readPoints, mapGrid, mapGrid4demo, outpathIMG
from astar_forUse import next_move
import numpy as np
from math  import sqrt
import time





def multiPointFlight(fname_pts:str, fname_start:str,commandFileName:str):
    start = time.time()
    intPts = readPoints(fname_pts)
    startPts = readPoints(fname_start)
    intpts_r = intPts[0].shape[0]
    print("intPts = "+str(intPts[0].shape[0]))
    distance = []
    print(intPts)
    j =0
    for r in range(int(intpts_r)):
        calc = sqrt((startPts[0][0]-intPts[0][j])**2+(startPts[1][0]-intPts[1][j])**2)
        print("calc = " +str(calc))
        print(distance)
        distance.append(calc)
        j+=1
    sorted_distance = sorted(distance)
    print("DIS = "+str(distance))
    print(sorted_distance)
    pt_order = [] 
    
    for j in range(len(sorted_distance)):
        for i in range(len(sorted_distance)):
            calc = sqrt((startPts[0][0]-intPts[0][i])**2+(startPts[1][0]-intPts[1][i])**2)
            if calc == sorted_distance[j]:
                pt_order.append(i)
    print(pt_order)
    grid = mapGrid(commandFileName)
    
    xint = []
    yint = []
    
    for order in pt_order:
        xint.append(intPts[0][order])
        yint.append(intPts[1][order])
        
    pts_pathNum = []
    xpts_planPath = []
    ypts_planPath = []
    l_xstartPts = startPts[0].tolist()
    l_ystartPts = startPts[1].tolist()
    print("-------------------------------------------")
    print(l_xstartPts, l_ystartPts)
    print("-------------------------------------------")
    xPts = l_xstartPts+xint+l_xstartPts
    yPts = l_ystartPts+yint+l_ystartPts
    print("-------------------------------------------")
    print(xPts, yPts)
    print("-------------------------------------------")
    #startPts__ = readPoints(fname_start)
    #xPts = xPts+startPts__[0].tolist()
    #yPts = yPts+startPts__[1].tolist()
    print(type(xPts))
    
    for i in range(len(pt_order)+1):
        print("Start X: "+str(xPts[i]))
        print("Start Y: "+str(yPts[i]))

        (pathNum, planPath) = next_move((xPts[i], yPts[i]),(xPts[i+1], yPts[i+1]), grid.tolist(), "path_5buff_75m_6pts_i0627.txt")
        pts_pathNum.append(pathNum)
        xpts_planPath+=planPath[0]
        ypts_planPath+=planPath[1]
        print("End X: "+str(xPts[i+1]))
        print("End Y: "+str(yPts[i+1]))
        print("\n")
    end = time.time()
    print(pts_pathNum)
    print(xpts_planPath)
    print(len(xpts_planPath))
    print("time is =="+str(end-start))
    respath = []
    respath.append(xpts_planPath)
    respath.append(ypts_planPath)
    grid4demo = mapGrid4demo(commandFileName)
    outpathIMG(grid,respath, xPts, yPts, "planpath_5buff_100m_6pts_ori0627_2")
    outpathIMG(grid4demo,respath, xPts, yPts, "planpath_5buff_100m_6pts_0627_2")
    
    
    
    


    
    



