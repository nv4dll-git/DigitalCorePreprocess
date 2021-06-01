#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2020 JIA Haowei, SWPU
E-mail contact: nv4dll@outlook.com
'''
import porespy as ps
import scipy as sp
import openpnm as op
import os
import imageio
import matplotlib.pyplot as plt
import numpy as np
#TODO test dat files in palabos
def overlappingspheres(shape,radius,porosity,filename,iter_max=0,getporousnetwork=False):
    r'''
    Generate a network from packing of overlapping mono-disperse spheres

    Parameters
    ----------
    shape : list
        The size of the image to generate in [Nx, Ny, Nz] where Ni is the
        number of voxels in the i-th direction.

    radius : int
        The radius of spheres in the packing.

    porosity : float
        The porosity of the final image, accurate to the given tolerance.

    iter_max : int
        Maximum number of iterations for the iterative algorithm that improves
        the porosity of the final image to match the given value.
    getporousnetwork : bool
        Save openpnm porousnetwork file
    '''
    im = ps.generators.overlapping_spheres(shape=shape, radius=radius, porosity=porosity, iter_max=iter_max)
    if shape[2] == 1 :
        plt.imshow(im[:, :, 0])
    else:
        plt.imshow(ps.visualization.sem(im))
    ps.io.to_palabos(im,filename)
    if getporousnetwork == True:
        snow = ps.networks.snow(im=im, voxel_size=1,boundary_faces=['top', 'bottom', 'left', 'right', 'front', 'back'])
        ps.io.to_openpnm(snow,filename+"_"+shape[0]+"_"+shape[1]+"_"+shape[2]+".dat")
    plt.show()
    
def polydispersespheres(shape,porosity,loc,scale,nbins,r_min,filename,getporousnetwork=False):

    dist = sp.stats.norm(loc=loc, scale=scale)
    im = ps.generators.polydisperse_spheres(shape,porosity,dist,nbins, r_min)
    if shape[2] == 1 :
        plt.imshow(im[:, :, 0])
    else:
        plt.imshow(ps.visualization.sem(im))
    ps.io.to_palabos(im,filename)
    if getporousnetwork == True:
        snow = ps.networks.snow(im=im, voxel_size=1,boundary_faces=['top', 'bottom', 'left', 'right', 'front', 'back'])
        ps.io.to_openpnm(snow,filename+"_"+shape[0]+"_"+shape[1]+"_"+shape[2]+".dat")
    plt.show()

def blobs(shape, porosity, blobiness, filename,getporousnetwork=False):

    im = ps.generators.blobs(shape=shape, porosity= porosity,blobiness=blobiness)
    if shape[2] == 1 :
        plt.imshow(im[:, :, 0])
    else:
        plt.imshow(ps.visualization.sem(im))
    ps.io.to_palabos(im,filename)
    if getporousnetwork == True:
        snow = ps.networks.snow(im=im, voxel_size=1,boundary_faces=['top', 'bottom', 'left', 'right', 'front', 'back'])
        ps.io.to_openpnm(snow,filename+"_"+shape[0]+"_"+shape[1]+"_"+shape[2]+".dat")
    plt.show()

def latticespheres(shape, radius,offset,lattice,filename,getporousnetwork=False):

    im = ps.generators.lattice_spheres(shape=shape, radius=radius, offset=offset, lattice=lattice)
    if len(shape) == 2:
        plt.imshow(im[:,:])
    else:
        plt.imshow(ps.visualization.sem(im))
    ps.io.to_palabos(im,filename)
    if getporousnetwork == True:
        snow = ps.networks.snow(im=im, voxel_size=1,boundary_faces=['top', 'bottom', 'left', 'right', 'front', 'back'])
        ps.io.to_openpnm(snow,filename+"_"+shape[0]+"_"+shape[1]+"_"+shape[2]+".dat")
    plt.show()

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

def insert(filename):

    blank = ps.generators.overlapping_spheres(shape=[170,170], radius=1, porosity=1)
    lattice = ps.generators.lattice_spheres(shape=[150,150], radius=13, offset=5, lattice='sc')
    # im = ps.generators.insert_shape(blank,lattice,center = [50,50])
    im = ps.generators.insert_shape(blank,lattice,corner = [20,20])
    plt.imshow(im[:,:])
    ps.io.to_palabos(im,filename)
    plt.show()

def dat2palabos(datname,filename,reversebool=False):
    '''
    Read file and return 2 numpy arrays. 
    Parameters
    ----------
    filename : str
    **reversebool : bool
        By changing reversebool=True, the user can reverse the meaning of True and False in bool_array
    Returns
    ----------
    bool_array : numpy array, in which True is represent for matrix and False is for porous.
    ascii_array : numpy array, in which '1' and '2' is represent for matrix and '0' is for porous.
    '''
    file = open(datname) #读取dat文件
    count = 0
    for index, line in enumerate(open(datname,'r')):
        count += 1
    dataslines = file.readlines()
    row = [ [] for i in range(count) ]
    for i in range (0,count):
        row[i] = dataslines[i].split(' ')

    if reversebool is False:
        for i in range(len(row)):
            for j in range(len(row[i])):
                if row[i][j] == '1' or row[i][j] == '2':
                    row[i][j] = 0
                else:
                    row[i][i] = 1

    else:
        for i in range(len(row)):
            for j in range(len(row[i])):
                if row[i][j] == '1' or row[i][j] == '2':
                    row[i][j] = 1
                else:
                    row[i][j] = 0
    bool_array = np.array(row) #储存row为bool

    outdata = []    
    for i in range(len(bool_array)):
        outdata.append(bool_array[i,:])

    ps.io.to_palabos(outdata,filename)
    plt.imshow(outdata[:,:])
    plt.show()

if __name__ == '__main__':

    overlappingspheres(shape=[200,200,1],radius=5,porosity=0.5,filename='100_100_100_30_porosity_test.dat',iter_max=5)
    # polydispersespheres(shape=[200,200,1],porosity=0.8,loc=8,scale=0.01,nbins= 50,r_min= 1, filename='test.dat')
    # blobs(shape=[50,50,50],porosity=0.6,blobiness=0.8, filename='blobs_50_50_50.dat')
    # latticespheres(shape=[87,87], radius=8,offset=3,lattice='fcc',filename='latticespheres_87_87_1.dat') #sc fcc bcc 
    # insert('imbibition_170_170_sc.dat')
    # dat2palabos('flat_surface_2d.dat','flat_surface_new_2.dat',reversebool=False)

