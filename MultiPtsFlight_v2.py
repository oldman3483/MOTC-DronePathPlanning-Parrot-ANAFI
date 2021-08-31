# -*- coding: utf-8 -*-
"""
Created on Sun May  9 18:25:36 2021

@author: ZXLi
"""

from utils_v2 import readMapInfo, mapGrid, mapGrid4demo, outpathIMG, writePath, writeHeight, checkPts
from astar_forUse import next_move
import numpy as np
from math  import sqrt
import time



def multiPointFlight(pj_name:str, start_Point:list, points_x:list, points_y:list, IsRelative:int, speed:float, buffsize:int, H_flight:float):
    start = time.time()
    mapInfo = readMapInfo("../data/mapInfo.txt")
    xCorner = float(mapInfo[2])
    yCorner = float(mapInfo[3])
    startPts = [start_Point[0][0]-float(xCorner), start_Point[1][0]-float(yCorner)]
    WarningMsg = []


    if startPts[0]-xCorner<0 or startPts[1]-yCorner<0:
        msg1 = "Reference points coordinates are wrong, check the start points"
        WarningMsg.append(msg1)
    
    if min(points_x)-xCorner<0 or min(points_y)-yCorner<0:
        msg1 = "Reference points coordinates are wrong, check the input points"
        WarningMsg.append(msg1)

    px = []
    py = []
    for i in range(len(points_x)):
        px.append(int(points_x[i]-float(xCorner)))
        py.append(int(points_y[i]-float(yCorner)))
    
    intPts = [px, py]
    intpts_r = len(intPts[0])
    print("intPts = "+str(intpts_r))
    distance = []
    print(intPts)
    j =0
    for r in range(int(intpts_r)):
        calc = sqrt((startPts[0]-intPts[0][j])**2+(startPts[1]-intPts[1][j])**2)
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
            calc = sqrt((startPts[0]-intPts[0][i])**2+(startPts[1]-intPts[1][i])**2)
            if calc == sorted_distance[j]:
                pt_order.append(i)
    print(pt_order)
    grid = mapGrid(H_flight)
    
    xint = []
    yint = []
    
    for order in pt_order:
        xint.append(intPts[0][order])
        yint.append(intPts[1][order])
        
    pts_pathNum = []
    xpts_planPath = []
    ypts_planPath = []
    l_xstartPts = [int(startPts[0])]
    l_ystartPts = [int(startPts[1])]
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
    grid4demo = mapGrid4demo(H_flight)
    outpathIMG(grid,respath, xPts, yPts, "Multi_"+pj_name+"_ori")
    outpathIMG(grid4demo,respath, xPts, yPts, "Multi_"+pj_name)
    writePath(xpts_planPath, ypts_planPath, "Multi_"+pj_name+"_path.txt", 'noUseNow')
    Hpts_planPath = writeHeight(xpts_planPath, ypts_planPath, pj_name+"_H2.txt",IsRelative ,H_flight)

    warning_index = checkPts(xpts_planPath, ypts_planPath, 30)
    WarningMsg.append("WARNING-----------------------"+str(warning_index)+" will be collided! --------------------------------")
    print(WarningMsg[-1])

    distance = 0
    photo_num = distance/speed

    

    return [xpts_planPath, ypts_planPath, Hpts_planPath, WarningMsg, speed, photo_num, distance]
    