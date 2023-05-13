import porespy as ps
import openpnm as op
import imageio
import matplotlib.pyplot as plt
import numpy as np

def image2dat(path,file_format,file_name,resolution,outputfilename,reversebool=None,getporousnetwork=False):
    r'''
    Generate a Generic network from image

    Parameters
    ----------
    path : str
        image file's path
    file_format : str
        image file's format,should be .tif
    file_name : str
        image file's name 
    resolution : float
        image file's  resolution
    reversebool : bool
        whether to reverse boolean value of image
    getporousnetwork : bool
        Save openpnm porousnetwork file
    '''
    #class extracepnm():
    # 1 for martix, 0 for porous
    file = file_name + file_format
    fetch_file = os.path.join(path, file)
    im = imageio.mimread(fetch_file)
    if reversebool == True:
        im = ~np.array(im, dtype=bool)
        print('reversed boolean value in imgae %s' % file_name)
    else:
        im = np.array(im, dtype=bool)
    #plt.imshow(im[:, :, shape[2]/2])
    plt.imshow(ps.visualization.sem(im))
    ps.io.to_palabos(im,outputfilename)
    if getporousnetwork == True:
        snow = ps.networks.snow(im=im, voxel_size=resolution,boundary_faces=['top', 'bottom', 'left', 'right', 'front', 'back'])
        ps.io.to_openpnm(snow,outputfilename)
    plt.show()

