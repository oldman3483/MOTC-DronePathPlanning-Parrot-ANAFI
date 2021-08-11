# -*- coding: utf-8 -*-
"""
Created on Sun July 9 12:01:31 2021

@author: ZXLi
"""

from utils import readPoints, mapGrid, mapGrid4demo, outpathIMG, IsObstalce, readmap, writePath, checkPts
from astar_forUse import next_move
from math  import sqrt, sin, cos
import time



def singlePointFlight(fname_pts:str, fname_start:str, commandFileName:str):
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

    print("-------------------------------------------")

    for i in range(0, 360, 2):
        xtmp = int(inPts[0]+cos(90-i)*radius)
        ytmp = int(inPts[1]+sin(90-i)*radius)

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
    grid = mapGrid()  # mapGrid will output the basic imforamtion of the map
    
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
    #print(pts_pathNum)
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

    grid4demo = mapGrid4demo()
    outpathIMG(grid,respath, xPts, yPts, "singlePts_5buff_75m_ang2_ori_harbor")
    outpathIMG(grid4demo,respath, xPts, yPts, "singlePts_5buff_ang2_75m_harbor")
    writePath(xpts_planPath, ypts_planPath, "singlePts_5buff_75m_ang2.txt", 'noUseNow')
    warning_index = checkPts(xpts_planPath, ypts_planPath, 30)
    print("WARNING-----------------------"+str(warning_index)+"--------------------------------")
    # output a txt file record the basic imfomation: warning msg, 
    # image TWD97 location base point

'''
def checkPts(xpath:list, ypath:list, Flight_height) -> list:
    # check whether each point is over the obstacle height setting 
    # return the indexes list which are over the height
    (mapinfo, map_arr) = readmap()

    res = []
    warning_xpts = []
    warning_ypts = []
    NoWarn = True
    for i in range(len(xpath)):
        if IsObstalce(map_arr[xpath[i]][ypath[i]], Flight_height, True):
            warning_xpts.append(xpath[i])
            warning_ypts.append(ypath[i])
            NoWarn = False

    if NoWarn: 
        print("SAFE FLIGHT")
        return 0
    else:
        res.append(warning_xpts)
        res.append(warning_ypts)
        print("WARNING!!!!! NEED TO INCREASE THE FLIGHT HEIGHT")

    return res
'''


