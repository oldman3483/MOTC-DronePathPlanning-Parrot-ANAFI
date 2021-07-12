# -*- coding: utf-8 -*-
"""
Created on Sun July 9 12:01:31 2021

@author: ZXLi
"""

from utils import readPoints, mapGrid, mapGrid4demo, outpathIMG, IsObstalce, readmap
from astar_forUse import next_move
from math  import sqrt, sin, cos
import time



def singlePointFlight(fname_pts:str, fname_start:str):
    start_time = time.time()
    inPts = readPoints(fname_pts)
    startPts = readPoints(fname_start)
    radius = 20  # need to be an input from reading file 
    grid = mapGrid()

    xin = []
    yin = []

#    xin+=l_xstartPts
#    yin+=l_ystartPts
    # x coordinate
    for i in range(0, 360, 45):
        xtmp = int(inPts[0]+cos(90-i)*radius)
        ytmp = int(inPts[1]+sin(90-i)*radius)

        xin.append(xtmp)
        yin.append(ytmp)
    
        print("xin: "+str(xin[int(i/45)]))
        print("yin: "+str(yin[int(i/45)]))

    # inputpts = checkPts(xin, yin)
    distance = []

    intpts_r = len(xin)
    for r in range(int(intpts_r)):
        calc = sqrt((xin[0]-xin[r])**2+(yin[0]-yin[r])**2)
        print("calc = " +str(calc))
        print(distance)
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
    grid = mapGrid()
    
    xin_sorted = []
    yin_sorted = []
    
    index = start_index
    for i in range(len(sorted_distance)):
        if index == len(sorted_distance):
            index = 0
        xin_sorted.append(xin[index])
        yin_sorted.append(yin[index])

        index+=1
    l_xstartPts = startPts[0].tolist()
    l_ystartPts = startPts[1].tolist()
    xin_sorted.append(xin[start_index])
    yin_sorted.append(yin[start_index])

    print("-------------------------------------------")
    xPts = l_xstartPts+xin_sorted+l_xstartPts
    yPts = l_ystartPts+yin_sorted+l_ystartPts
    
    print("-------------------------------------------")
    print(xPts, yPts)
    print("-------------------------------------------")
    print(type(xPts))

    pts_pathNum = []
    xpts_planPath = []
    ypts_planPath = []
    for i in range(len(sorted_distance)+2):
        print("Start X: "+str(xPts[i]))
        print("Start Y: "+str(yPts[i]))

        (pathNum, planPath) = next_move((xPts[i], yPts[i]),(xPts[i+1], yPts[i+1]), grid.tolist(), "singlePts_5buff_100m_0711.txt")
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
    print("time is =="+str(end_time-start_time))
    respath = []
    respath.append(xpts_planPath)
    respath.append(ypts_planPath)
    grid4demo = mapGrid4demo()
    outpathIMG(grid,respath, xPts, yPts, "singlePts_5buff_100m_ori0711")
    outpathIMG(grid4demo,respath, xPts, yPts, "singlePts_5buff_100m_0711")
    


def checkPts(xlist:list, ylist:list) -> list:
    res_pts = []

    return res_pts


def find8direction(x:int, y:int) -> list:
    res = []
    
    


    return res

    