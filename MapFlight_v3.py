# -*- coding: utf-8 -*-
"""
Created on Sun July 18 16:39:07 2021

@author: ZXLi
"""
from utils_v2 import readMapInfo, mapGrid, mapGrid4demo, outpathIMG, writePath, checkPts, writeHeight
from astar_forUse import next_move
import numpy as np
import time

def mapSurveyFlight(pj_name:str, start_Point:list, points_x:list, points_y:list, IsRelative:int, speed:float, buffsize:int, H_flight:float):
    start_time = time.time()
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
    
    inPts = [px, py]
    minYpts = min(inPts[1])
    maxYpts = max(inPts[1])
    minXpts = min(inPts[0])
    maxXpts = max(inPts[0])
    xstep = 10
    
    ystep = 15
    i_minY = findIndex(inPts[1], minYpts)
    if i_minY == -1:
        print("-------------- Wrong in function findIndex!! ------------")

    pt_order = []
    pt_order.append(i_minY)
    
    xin = []
    yin = []
    xin.append(inPts[0][i_minY])
    yin.append(inPts[1][i_minY])
    while (yin[-1] < maxYpts):
        '''
        if yin[-1] < maxYpts and (yin[-1]+ystep) < maxYpts:
            x_coor = xin[-1] 
            y_coor = yin[-1]+ystep
            xin.append(x_coor)
            yin.append(y_coor)
        else: break
        '''
        while  (xin[-1] < maxXpts and (xin[-1]+xstep) < maxXpts):
            x_coor = xin[-1] + xstep
            y_coor = yin[-1]
            xin.append(x_coor)
            yin.append(y_coor)
        if yin[-1] < maxYpts and (yin[-1]+ystep) < maxYpts:
            x_coor = xin[-1] 
            y_coor = yin[-1]+ystep
            xin.append(x_coor)
            yin.append(y_coor)
        else: break
        while  (xin[-1] > minXpts and (xin[-1]-xstep) > minXpts):
            x_coor = xin[-1] - xstep
            y_coor = yin[-1]
            xin.append(x_coor)
            yin.append(y_coor)
        if yin[-1] < maxYpts and (yin[-1]+ystep) < maxYpts:
            x_coor = xin[-1] 
            y_coor = yin[-1]+ystep
            xin.append(x_coor)
            yin.append(y_coor)
        else: break
    print ("x coor : "+str(xin))
    grid = mapGrid(H_flight)
    # drawPtsOnGrid (grid, xin, yin, "planpath_mapsurvey_test")
    l_xstartPts = [int(startPts[0])]
    l_ystartPts = [int(startPts[1])]
    
    xPts = l_xstartPts+[xin[0]]
    yPts = l_ystartPts+[yin[0]]
    print("-------------------------------------------")
    pts_pathNum = []
    xpts_planPath = []
    ypts_planPath = []
    for i in range(1):
        print("Start X: "+str(xPts[i]))
        print("Start Y: "+str(yPts[i]))
        print("End X: "+str(xPts[i+1]))
        print("End Y: "+str(yPts[i+1]))
        print("\n")
        (pathNum, planPath) = next_move((xPts[i], yPts[i]),(xPts[i+1], yPts[i+1]), grid.tolist(), "MapSurvey_5buff_100m_0722.txt")
        pts_pathNum.append(pathNum)
        xpts_planPath+=planPath[0]
        ypts_planPath+=planPath[1]
        #print("End X: "+str(xPts[i+1]))
        #print("End Y: "+str(yPts[i+1]))
        #print("\n")

    xPts_back = [xin[-1]]+[xin[0]]
    yPts_back = [yin[-1]]+[yin[0]]
    print("-------------------------------------------")
    pts_pathbackNum = []
    xpts_planPath_back = []
    ypts_planPath_back = []
    for i in range(1):
        print("Start X: "+str(xPts_back[i]))
        print("Start Y: "+str(yPts_back[i]))
        print("End X: "+str(xPts_back[i+1]))
        print("End Y: "+str(yPts_back[i+1]))
        print("\n")
        (pathNum_back, planPath_back) = next_move((xPts_back[i], yPts_back[i]),(xPts_back[i+1], yPts_back[i+1]), grid.tolist(), "noUse")
        pts_pathbackNum.append(pathNum_back)
        xpts_planPath_back+=planPath_back[0]
        ypts_planPath_back+=planPath_back[1]
    end_time = time.time()
    xpts_planPath += xin+xpts_planPath_back
    ypts_planPath += yin+ypts_planPath_back
    
    print("Go path NUM ->>> "+ str(pathNum))
    print("-------------------------------------------")
    print("back path NUM ->>> "+ str(pathNum_back))
    print("xin ---------------------------------------------")
    print(xin)
    print("yin ->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(yin)
    print("-------------------------------------------")
    print((len(xpts_planPath)-pathNum-pathNum_back)*xstep+ystep*6)
    print("Fly distance ==>>> " + str(((len(xpts_planPath)-pathNum-pathNum_back)*xstep+ystep*6)+pathNum+pathNum_back))
    print("time is =="+str(end_time-start_time))
    respath = []
    respath.append(xpts_planPath)
    respath.append(ypts_planPath)

    print("-------------------------------------------")
    print(respath)
    print("-------------------------------------------")


    grid4demo = mapGrid4demo(H_flight)
    outpathIMG(grid,respath, xPts, yPts, "Map_"+pj_name+"_ori")
    outpathIMG(grid4demo,respath, xPts, yPts, "Map_"+pj_name)
    writePath(xpts_planPath, ypts_planPath, "Map_"+pj_name+"_path.txt", 'noUseNow')
    Hpts_planPath = writeHeight(xpts_planPath, ypts_planPath, pj_name+"_H2.txt",IsRelative ,H_flight)

    warning_index = checkPts(xpts_planPath, ypts_planPath, 30)
    WarningMsg.append("WARNING-----------------------"+str(warning_index)+" will be collided! --------------------------------")
    print(WarningMsg[-1])

    distance = ((len(xpts_planPath)-pathNum-pathNum_back)*xstep+ystep*6)+pathNum+pathNum_back
    photo_num = distance/speed

    

    return [xpts_planPath, ypts_planPath, Hpts_planPath, WarningMsg, speed, photo_num, distance]
def findIndex(pts:list, value:int):
    
    for i in  range(len(pts)):
        if value == pts[i]:
            return i

    return -1 


