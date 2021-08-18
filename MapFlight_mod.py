# -*- coding: utf-8 -*-
"""
Created on Sun July 18 16:39:07 2021

@author: ZXLi
"""
from utils import drawPtsOnGrid, readPoints, mapGrid, mapGrid4demo, outpathIMG, writePath, checkPts, readCmd
from astar_forUse import next_move
import numpy as np
from math  import sqrt
import time

def mapSurveyFlight(fpts_map:str, fpts_start:str, commandFileName:str):
    start_time = time.time()
    mapinfo = readCmd("../data/mapInfo.txt")
    startPts = readPoints(fpts_start)
    
    #if (startPts[0]-mapinfo[2] <0) or (startPts[1]-mapinfo[3] <0):
    #    print("---------warnning------------Start Point is out of bound !!----------")
    #    return 0
    inPts = readPoints(fpts_map)
    intpts_r = inPts[0].shape[0]
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
    grid = mapGrid(commandFileName)
    # drawPtsOnGrid (grid, xin, yin, "planpath_mapsurvey_test")
    l_xstartPts = startPts[0].tolist()
    l_ystartPts = startPts[1].tolist()
    
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


    grid4demo = mapGrid4demo(commandFileName)
    outpathIMG(grid,respath, xPts, yPts, "Harbor_img_ori")
    outpathIMG(grid4demo,respath, xPts, yPts, "Harbor_img")
    writePath(xpts_planPath, ypts_planPath, "MapSurvey_5buff_75m.txt", 'noUseNow')
    warning_index = checkPts(xpts_planPath, ypts_planPath, 30)
    print("WARNING-----------------------"+str(warning_index)+"--------------------------------")
        

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


