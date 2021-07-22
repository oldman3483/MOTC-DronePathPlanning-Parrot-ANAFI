# -*- coding: utf-8 -*-
"""
Created on Sun July 18 16:39:07 2021

@author: ZXLi
"""
from utils import drawPtsOnGrid, readPoints, mapGrid, mapGrid4demo, outpathIMG
from astar_forUse import next_move
import numpy as np
from math  import sqrt
import time

def mapSurveyFlight(fpts_map:str, fpts_start:str):
    start_time = time.time()
    startPts = readPoints(fpts_start)
    inPts = readPoints(fpts_map)
    intpts_r = inPts[0].shape[0]
    minYpts = min(inPts[1])
    maxYpts = max(inPts[1])
    minXpts = min(inPts[0])
    maxXpts = max(inPts[0])
    xstep = 20
    ystep = 10
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
        if yin[-1] < maxYpts and (yin[-1]+ystep) < maxYpts:
            x_coor = xin[-1] 
            y_coor = yin[-1]+ystep
            xin.append(x_coor)
            yin.append(y_coor)
        else: break
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
    grid = mapGrid()
    # drawPtsOnGrid (grid, xin, yin, "planpath_mapsurvey_test")
    l_xstartPts = startPts[0].tolist()
    l_ystartPts = startPts[1].tolist()
    
    xPts = l_xstartPts+xin+l_xstartPts
    yPts = l_ystartPts+yin+l_ystartPts
    print("-------------------------------------------")
    pts_pathNum = []
    xpts_planPath = []
    ypts_planPath = []
    for i in range(len(xin)+1):
        #print("Start X: "+str(xPts[i]))
        #print("Start Y: "+str(yPts[i]))

        (pathNum, planPath) = next_move((xPts[i], yPts[i]),(xPts[i+1], yPts[i+1]), grid.tolist(), "MapSurvey_5buff_100m_0722.txt")
        pts_pathNum.append(pathNum)
        xpts_planPath+=planPath[0]
        ypts_planPath+=planPath[1]
        #print("End X: "+str(xPts[i+1]))
        #print("End Y: "+str(yPts[i+1]))
        #print("\n")
    end_time = time.time()
    print(pts_pathNum)
    print(xpts_planPath)
    print(len(xpts_planPath))
    print("time is =="+str(end_time-start_time))
    respath = []
    respath.append(xpts_planPath)
    respath.append(ypts_planPath)
    grid4demo = mapGrid4demo()
    outpathIMG(grid,respath, xPts, yPts, "MapSurvey_5buff_100m_ori0722")
    outpathIMG(grid4demo,respath, xPts, yPts, "MapSurvey_5buff_100m_0722")
    print("test git push")
        

def findClosePt(xpts:list, ypts:list, x:int, y:int):
    res_i = -1
    dis = []
    min = 1000000
    for i in range(len(xpts)):
        value = sqrt((x-xpts[i])**2+(y-ypts[i])**2)
        if value<min:
            min = value
            res_i = i

    return res_i





def findIndex(pts:list, value:int):
    
    for i in  range(len(pts)):
        if value == pts[i]:
            return i

    return -1 


