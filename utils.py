
import numpy as np
import cv2 as cv
import math

def readCmd(cmdFileName):
    cmd = open(cmdFileName, 'r')
    
    for line in cmd.readlines():
        r_list = line.split(',')
        j = 0
        print("line== "+str(line))
        print("r_list== "+str(r_list))
    

    # cmd file write format [IsRelativeHeight, FlightHeight, ]
    return r_list


def readPoints(fname:str) -> (object):
    fpts = open(fname, 'r')
    
    pts_num = 0
    for line in fpts.readlines():
        pts_num+=1
    fpts.close()
    
    print(pts_num)
    ptsx = []
    ptsy = []
    
    fpts = open(fname, 'r')
    row = 0
    for line in fpts.readlines():
        r_list = line.split(',')
        j = 0
        #print("line"+str(line))
        #print("r_list"+str(r_list))
        
        #for conp in r_list:
        if(r_list[0]!='\n'):
            ptsx.append(int(r_list[0]))
            ptsy.append(int(r_list[1]))
        
        row+=1
    ptsCor = np.array((ptsx, ptsy))
    return ptsCor    

def readmap() -> object:
    filename = "../data/1m_harbor.txt"#xyz_1m.txt"
    maptxt = open(filename, mode='r')
    ncols = int(splitNum(maptxt.readline()))
    nrows = int(splitNum(maptxt.readline()))
    xCorner = float(splitNum(maptxt.readline()))
    yCorner = float(splitNum(maptxt.readline()))
    maptxt.readline() #cell size
    noData = int(splitNum(maptxt.readline()))
    
    mapINFO = np.array([nrows, ncols, xCorner, yCorner, noData])
    
    map_arr = np.zeros((nrows, ncols), dtype=np.float32)
    
    i = 0
    
    for line in maptxt.readlines():
        row_list = np.asarray(line.split(sep=' '))
        j = 0
        for height in row_list:    
            if(height != '\n'):
                map_arr[i][j]= float(height)
            j+=1
        
        #print(map_arr[i][100:200])
        i+=1
        
    return (mapINFO, map_arr)


# declare global varible 

xCorner = 0.0
yCorner = 0.0


def mapGrid() -> (object):
    (mapinfo, map_arr) = readmap()
    H_flight = 30 #set default 30m 
    
    global xCorner, yCorner

    nrows = int(mapinfo[0])
    ncols = int(mapinfo[1])
    xCorner = mapinfo[2]
    yCorner = mapinfo[3]
    noData = mapinfo[-1]

    out_map = np.empty((int(nrows), int(ncols)), dtype=str)


# use list is better choice or check the dtype of the np.string_
    for r in range(nrows):
        for c in range(ncols):
            if int(map_arr[r][c]) == noData:
                out_map[r][c] = '.'
                #continue
            elif IsObstalce(map_arr[r][c], H_flight, True):
                setObstacle(out_map, r, c, 5)
            else:
                out_map[r][c] = '.'

    return out_map

def mapGrid4demo() -> (object):
    (mapinfo, map_arr) = readmap()
    H_flight = 30 #set default 30m 


    nrows = int(mapinfo[0])
    ncols = int(mapinfo[1])
    #xCorner = mapinfo[2]
    #yCorner = mapinfo[3]
    noData = mapinfo[-1]

    out_map = np.empty((int(nrows), int(ncols)), dtype=str)


# use list is better choice or check the dtype of the np.string_
    for r in range(nrows):
        for c in range(ncols):
            if int(map_arr[r][c]) == noData:
                out_map[r][c] = '.'
                #continue
                
            elif IsObstalce(map_arr[r][c], H_flight, True):
                out_map[r][c] = '%'
            else:
                out_map[r][c] = '.'

    return out_map





def IsObstalce(height:float, H_flight: float, default:bool) -> (bool):
	if ((height+H_flight) > 75) and default:
		return True
	return False


    
def splitNum(str_num):
    data = str_num.split(' ')
    return data[-1]
    
def outpathIMG(grid: object, planPath:list, xpts:list, ypts:list, outfname:str):
    
    (r_, c_) = grid.shape
    img_arr = np.zeros((r_, c_, 3), dtype=np.int16)
    for r in range(r_):
        for c in range(c_):
            if(grid[r][c] == '.'):
                img_arr[r][c][0] = 220
                img_arr[r][c][1] = 220
                img_arr[r][c][2] = 220
            elif(grid[r][c] == '%'):
                SetPixel3band(img_arr, r, c, 0, 0, 0)

    for r in range(len(planPath[0])):
        img_arr[planPath[0][r]][planPath[1][r]][0] = 0   #B
        img_arr[planPath[0][r]][planPath[1][r]][1] = 155 #G
        img_arr[planPath[0][r]][planPath[1][r]][2] = 255 #R
    
    
    for pts in range(len(xpts)):
        SetPixel3band(img_arr, xpts[pts], ypts[pts], 0, 0, 255)
    
    cv.imwrite("../output/map/"+str(outfname)+".png", img_arr)

def drawPtsOnGrid(grid:object, xpts:list, ypts:list, fname:str):
    (r_, c_) = grid.shape
    img_arr = np.zeros((r_, c_, 3), dtype=np.int16)
    for r in range(r_):
        for c in range(c_):
            if(grid[r][c] == '.'):
                img_arr[r][c][0] = 220
                img_arr[r][c][1] = 220
                img_arr[r][c][2] = 220
            elif(grid[r][c] == '%'):
                SetPixel3band(img_arr, r, c, 0, 0, 0)
    for pts in range(len(xpts)):
        SetPixel3band(img_arr, xpts[pts], ypts[pts], 0, 0, 255)
    
    cv.imwrite("../output/map/"+str(fname)+".png", img_arr)



def SetPixel3band(img_arr:object, r:int, c:int, B:int, G:int, R:int):
    try:
        img_arr[r][c][0] = B
        img_arr[r][c][1] = G
        img_arr[r][c][2] = R
    except IndexError:
        pass
    
    
def setObstacle(img_arr:object, r:int, c:int, bufsize:int):
    try:
        for i in range(bufsize):
            for j in range(bufsize):
            
                img_arr[r-i][c]='%'
                img_arr[r-i][c+j]='%'
                img_arr[r-i][c-j]='%'
                
                img_arr[r+i][c]='%'
                img_arr[r+i][c+j]='%'
                img_arr[r+i][c-j]='%'
                
                img_arr[r][c+j]='%'
                img_arr[r][c-j]='%'
    
    except IndexError:
        print("error")
        pass
def writePath(xpath:list, ypath:list, fname:str, input_name:str):
# use the global varible xCorner and yCorner instead the read the input_name file


    path_txt = open("../output/planningpath/"+fname, 'w')
    path_txt.write(str(xpath[:]+xCorner))
    path_txt.write('\n')
    path_txt.write(str(ypath[:]+yCorner))

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