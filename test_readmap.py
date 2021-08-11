import cv2 as cv
import time
from utils import readmap, readCmd

def readmap_2():
    fname = ".txt"
    with open(fname, 'r', encoding='utf-8') as f:
        for chunk in iter(lambda: f.read(1024), ''):
            print(chunk)


def readmap_pic():
    start_time = time.time()
    fname = "../data/harbor_dsm.png"
    data = cv.imread(fname, 0)
    end_time = time.time()
    print(data.shape)
    print(data[0:10][0:10])
    print("read time = "+str(end_time-start_time))
    print(max(data.tolist()))
    cv.imshow("dsm", data)
    cv.waitKey(3000)
    cv.destroyAllWindows()




def main():
    readmap_pic()
    #readmap()
    #readCmd("../data/mapInfo.txt")
if __name__ ==  '__main__':
    main() 