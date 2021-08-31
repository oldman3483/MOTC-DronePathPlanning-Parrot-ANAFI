# -*- coding: utf-8 -*-
"""
Created on Sun July 9 11:48:45 2021

@author: ZXLi
"""

from MultiPtsFlight import multiPointFlight
from SinglePtFlight_v3 import singlePointFlight
from  MapFlight_mod import  mapSurveyFlight



def main():
    Project_Name = ""
    mode = 0
    start_point = [[],[]] # input list of the start points coordinates
    fname_start = '../data/startCor.txt'
    

    # can be changed and need a default value
    speed = 3.0
    H_flight = 30
    IsRelative = 0
    buffsize = 6

      
    if mode == 1:
        fname_pts = '../data/multipoints_default_6pts.txt'   #multipoints_default_t2.txt'
        multiPointFlight(fname_pts, fname_start)
    elif mode == 2:
        points_x = []
        points_y = []
        singlePointFlight(start_point, points_x, points_y, IsRelative, speed, buffsize, H_flight)
    elif mode == 3:
        fpts_map = '../data/mapFlightPts_test.txt'#mapFlightPts_default.txt'
        mapSurveyFlight(fpts_map, fname_start)
    '''
    if mode == 1:
        fname_pts = '../data/multipoints_default_6pts.txt'   #multipoints_default_t2.txt'
        multiPointFlight(fname_pts, fname_start)
    elif mode == 2:
        fpts_single = '../data/SinglePoints_default.txt'
        singlePointFlight(fpts_single, fname_start,'../data/flightCmd.txt')
    elif mode == 3:
        fpts_map = '../data/mapFlightPts_test.txt'#mapFlightPts_default.txt'
        mapSurveyFlight(fpts_map, fname_start)
    '''

    

if __name__ == '__main__':
   
    main()