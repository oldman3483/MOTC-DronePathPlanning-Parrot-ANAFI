from utils import readmap
import numpy as np
import cv2 as cv
import time

def writemap(mapname):
    start_time = time.time()
    (map_info, map_arr) = readmap()
    (r_, c_) = map_arr.shape
    print(r_, c_)
    cv.imwrite("../data/"+str(mapname)+".png", map_arr)
    end_time = time.time()
    print("read time = "+str(end_time-start_time))

def main():
    writemap("harbor_test")

if __name__ == '__main__':
    main()