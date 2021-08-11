import cv2 as cv
import time
from utils import readmap

def readmap_2():
    fname = ".txt";
    with open(fname, 'r', encoding='utf-8') as f:
        for chunk in iter(lambda: f.read(1024), ''):
            print(chunk)


def readmap_pic():
    start_time = time.time()
    fname = "../data/Harbor_all_ori.png"
    data = cv.imread(fname)
    end_time = time.time()
    print(data.shape)
    print(data[0:10][0:10])
    print("read time = "+str(end_time-start_time))





def main():
    #readmap_pic()
    #readmap()

if __name__ ==  '__main__':
    main() 