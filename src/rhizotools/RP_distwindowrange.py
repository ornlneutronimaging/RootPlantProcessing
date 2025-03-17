import numpy as np

def RP_distwindowrange(i,j,windowsize,imdim):
    '''
    SUMMARY:
    'RPdistwindowrange':outputs rows/columns after considering edge effects for a single
    pixel distance array.  Used only in 'RPthickness' code.  
    
    USING CODE: 
    Position 'i' (i.e. rows) and 'j' (i.e. columns) will be evaluated in conjunction with 
    the evaluated window size 'windowsize', and ensure that the rows/columns outputted 
    do not exceed image dimensions specified by 'imdim'.  Code will include last number 
    to be excluded.  
    
    PARAMETERS: 
    A. INPUTS - 
    1. i: row position for the center of the window (y).
    2. j: column position for the center of the window (x).
    3. windowsize: 1D-size of the window.  Must be odd numbered. 
    4. imdim: image dimensions - row, column.
    
    B. OUTPUTS -
    1. y1: starting row position for evaluated window.
    2. y2: ending row position for evaluated window.
    3. x1: starting column position for evaluated window.
    4. x2: ending column position for evaluated window.
    5. yc: center row position for evaluated window.
    6. xc: center column position for evaluated window.
    
    
    EXAMPLE:
    For a 10x10 array and a window size of 3, evaluating a position at [5,6], 'i' and 
    'j' will correspond to 5 and 7, 'windowsize' will correspond to 3, and 'imdim' will 
    correspond to [10, 10].  In this case, outputs will correspond to y1=0,y2=8,x1=0,x2=8,yc=3,xc=3.  
    
    If i and j were [1,1], then y1=2,y2=8,x1=2,x2=8,yc=1,xc=1.
    '''
    
    windowsize = np.floor(windowsize/2)
    
    y1 = 0
    y2 = windowsize*2+2
    yc = windowsize
    
    if i < windowsize:
        y1 = windowsize-i
        yc = i
    elif i >= imdim[0]-windowsize:
        y2 = windowsize+(imdim[0]-i)+1
    
    x1 = 0
    x2 = windowsize*2+2
    xc = windowsize
    
    if j < windowsize:
        x1 = windowsize-j
        xc = j
    elif j >= imdim[1]-windowsize:
        x2 = windowsize+(imdim[1]-j)+1
        
    y1 = int(y1)
    y2 = int(y2)
    x1 = int(x1)
    x2 = int(x2)
    yc = int(yc)
    xc = int(xc)
        
    return (y1,y2,x1,x2,yc,xc)    