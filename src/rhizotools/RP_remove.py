import numpy as np

def RP_remove(image, connection=4,edge=True):
    '''
    SUMMARY: 
    'RP_remove': creates a contour image of the original by removing all center pixels.  
    
    USING CODE:
    The inputted binary image will be checked at all true pixels to confirm 4- or 8-connection.
    If valid, then this pixel will be considered a non-contour pixel and not included.  'edge' 
    affirms whether any objects that terminate on the edge of the image should be considered 
    'closed' (i.e. fully within the image) or 'open' (i.e. continues outside
    the image) object.  If the object is considered 'open' (i.e. True), then the contour pixels
    will not fully wrap around the object.
    
    PARAMETERS:
    1. image: binary image to be analyzed.
    2. connection: scalar value that specifies what connection to be used.  Either 4 or 8 is valid.
    3. edge: flag confirming whether objects on edge of image are considered 'open' or 'closed'.
    Takes values of 'TRUE' (open) or 'FALSE' (closed).
    
    '''

    imagepos = np.where(image)
    imagepos_y = imagepos[0]+1
    imagepos_x = imagepos[1]+1
    
    imdim = np.shape(image)
    if edge:
        img = np.ones([imdim[0]+2, imdim[1]+2])
    else:
        img = np.zeros([imdim[0]+2, imdim[1]+2])
    
    finalimg = np.zeros([imdim[0]+2,imdim[1]+2])
    img[1:imdim[0]+1,1:imdim[1]+1] = image
    
    if connection == 4:
        for i in range(np.shape(imagepos_y)[0]):
            x = imagepos_x[i]
            y = imagepos_y[i]
            if (img[y-1,x]+img[y+1,x]+img[y,x-1]+img[y,x+1]) == 4:
                continue
            else:
                finalimg[y,x] = 1
    
    if connection == 8:
        for i in range(np.shape(imagepos_y)[0]):
            x = imagepos_x[i]
            y = imagepos_y[i]
            if (img[y-1,x]+img[y+1,x]+np.sum(img[y-1:y+2,x-1])+np.sum(img[y-1:y+2,x+1])) == 8:
                continue
            else:
                finalimg[y,x] = 1
    
    finalimg = finalimg[1:imdim[0]+1,1:imdim[1]+1]
    
    return finalimg
