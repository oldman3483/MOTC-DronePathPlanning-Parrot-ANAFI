# -*- coding: utf-8 -*-
"""
Created on Sun July 9 11:48:45 2021

@author: ZXLi
"""

from MultiPtsFlight import multiPointFlight
from SinglePtFlight import singlePointFlight

def main():
    fname_start = '../data/startCor.txt'
    fname_pts = '../data/multipoints_default_6pts.txt'   #multipoints_default_t2.txt'
    #multiPointFlight(fname_pts, fname_start)
    fpts_single = '../data/SinglePoints_default.txt'
    singlePointFlight(fpts_single, fname_start)



if __name__ == '__main__':
   
    main()