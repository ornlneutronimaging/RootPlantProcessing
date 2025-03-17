import numpy as np

def RP_windowrange(i,j,windowsize,imdim):
    '''
    SUMMARY:
    'RP_windowrange': outputs rows/columns after considering edge effects based on current x/y
    position and image size.
    
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
    
    
    EXAMPLE:
    For a 10x10 array and a window size of 3, evaluating a position at [5,6], 'i' and 
    'j' will correspond to 5 and 7, 'windowsize' will correspond to 3, and 'imdim' will
    correspond to [10, 10].  In this case, outputs will correspond to y1=2,y2=9,x1=3,x2=10.  
    
    If i and j were [7,8], then y1=4,y2=10,x1=5,x2=10.
    
    '''
    windowsize = np.floor(windowsize/2)
    
    y1 = i-windowsize
    y2 = i+windowsize+1
    if i < windowsize:
        y1 = 0
        y2 = i+windowsize+1
    elif i >= imdim[0]-windowsize:
        y1 = i-windowsize
        y2 = imdim[0]
    
    x1 = j-windowsize
    x2 = j+windowsize+1
    if j < windowsize:
        x1 = 0
        x2 = j+windowsize+1
    elif j >= imdim[1]-windowsize:
        x1 = j-windowsize
        x2 = imdim[1]
    
    y1 = int(y1)
    y2 = int(y2)
    x1 = int(x1)
    x2 = int(x2)
    
    return (y1,y2,x1,x2)
