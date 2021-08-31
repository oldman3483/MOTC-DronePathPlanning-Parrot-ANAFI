# -*- coding: utf-8 -*-
"""
Created on Sun July 9 12:01:31 2021

@author: ZXLi
"""

from utils_v2 import readMapInfo, mapGrid, mapGrid4demo, outpathIMG, IsObstalce, readmap, writeHeight, writePath, checkPts
from astar_forUse import next_move
from math  import sqrt, sin, cos
import time


# cmd file write format [IsRelativeHeight, FlightHeight, ]
def singlePointFlight(pj_name:str, start_Point:list, points_x:list, points_y:list, IsRelative:int, speed:float, buffsize:int, H_flight:float):
    start_time = time.time()
    WarningMsg = []
    mapInfo = readMapInfo("../data/mapInfo.txt")
    xCorner = float(mapInfo[2])
    yCorner = float(mapInfo[3])

    startPts = start_Point
    radius = 20  # need to be an input from reading file 
    
    xin = []
    yin = []

#    xin+=l_xstartPts
#    yin+=l_ystartPts
#    x coordinate
    if startPts[0][0]-xCorner<0 or startPts[1][0]-yCorner<0:
        msg1 = "Reference points coordinates are wrong, check the start points"
        WarningMsg.append()
    
    if points_x[0]-xCorner<0 or points_y[0]-yCorner<0:
        msg1 = "Reference points coordinates are wrong, check the input points"
        WarningMsg.append()
        
    print("-------------------------------------------")

    for i in range(0, 360, 2):
        xtmp = int(points_x[0]-xCorner+cos(90-i)*radius)
        ytmp = int(points_y[0]-yCorner+sin(90-i)*radius)

        xin.append(xtmp)
        yin.append(ytmp)
    
        print("xin: "+str(xin[int(i/2)]))
        print("yin: "+str(yin[int(i/2)]))
    print("-------------------------------------------")

    # inputpts = checkPts(xin, yin)
    distance = []

    intpts_r = len(xin)
    for r in range(int(intpts_r)):
        calc = sqrt((xin[0]-xin[r])**2+(yin[0]-yin[r])**2)
        #print("calc = " +str(calc))
        #print(distance)
        distance.append(calc)
    
    sorted_distance = sorted(distance)
    print("DIS = "+str(distance))
    print(sorted_distance)
    
    start_index = 0

    for i in range(len(sorted_distance)):
        calc = sqrt((xin[0]-xin[i])**2+(yin[0]-yin[i])**2)
        if calc == sorted_distance[0]:
            start_index = i
    print(start_index)
    grid = mapGrid(H_flight)  # mapGrid will output the basic imforamtion of the map
    xin_sorted = []
    yin_sorted = []
    
    index = start_index
    for i in range(len(sorted_distance)):
        if index == len(sorted_distance):
            index = 0
        xin_sorted.append(xin[index])
        yin_sorted.append(yin[index])

        index+=1
    l_xstartPts = [int(startPts[0][0] - xCorner)]
    l_ystartPts = [int(startPts[1][0] - yCorner)]
    xin_sorted.append(xin[start_index])
    yin_sorted.append(yin[start_index])

    print(xin_sorted)

    print("-------------------------------------------")
    xPts = l_xstartPts+[xin_sorted[1]]
    yPts = l_ystartPts+[yin_sorted[1]]
    
    print("-------------------------------------------")
    print(xPts, yPts)
    print("-------------------------------------------")
    print(type(xPts))

    pts_pathNum = []
    xpts_planPath = []
    ypts_planPath = []
    for i in range(1):
        print("Start X: "+str(xPts[i]))
        print("Start Y: "+str(yPts[i]))

        (pathNum, planPath) = next_move((xPts[i], yPts[i]),(xPts[i+1], yPts[i+1]), grid.tolist(), "singlePts_5buff_75m_ang2.txt")
        pts_pathNum.append(pathNum)
        xpts_planPath+=planPath[0]
        ypts_planPath+=planPath[1]
        print("End X: "+str(xPts[i+1]))
        print("End Y: "+str(yPts[i+1]))
        print("\n")
    end_time = time.time()
    print(pts_pathNum)
    print(xpts_planPath)
    print(len(xpts_planPath))
    xpts_planPath_back = list(reversed(xpts_planPath))
    ypts_planPath_back = list(reversed(ypts_planPath))
    xpts_planPath += xin + xpts_planPath_back
    ypts_planPath += yin +ypts_planPath_back
    print("-------------------------------------------")
    print(xpts_planPath)
    print("-------------------------------------------")

    print("time is =="+str(end_time-start_time))
    respath = []
    respath.append(xpts_planPath)
    respath.append(ypts_planPath)


    print("-------------------------------------------")
    print(respath)
    print("-------------------------------------------")

    
    grid4demo = mapGrid4demo(H_flight)
    outpathIMG(grid,respath, xPts, yPts, pj_name+"_ori")
    outpathIMG(grid4demo,respath, xPts, yPts, pj_name)
    print("-------------------------------------------")
    writePath(xpts_planPath, ypts_planPath, pj_name+"_path.txt", 'noUseNow')
    wpathtime = time.time()
    print("complete writePath  time= " + str(wpathtime-end_time))
    print("-------------------------------------------")
    Hpts_planPath = writeHeight(xpts_planPath, ypts_planPath, pj_name+"_H2.txt",IsRelative ,H_flight)
    wHpathtime = time.time()
    print("complete write Height Path  time= " + str(wHpathtime-end_time))
    print("-------------------------------------------")
    warning_index = checkPts(xpts_planPath, ypts_planPath, 30)
    WarningMsg.append("WARNING-----------------------"+str(warning_index)+" will be collided! --------------------------------")
    print(WarningMsg[-1])
    # output a txt file record the basic imfomation: warning msg, 
    # image TWD97 location base point



