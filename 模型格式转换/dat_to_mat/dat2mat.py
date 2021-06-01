#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2020 JIA Haowei
E-mail contact: nv4dll@outlook.com
'''
import time
import numpy as np
import scipy.io
import copy

def datreader(filename,reversebool):
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
	file = open(filename) #读取dat文件
	count = 0
	for index, line in enumerate(open(filename,'r')):
		count += 1
	dataslines = file.readlines()
	row = [ [] for i in range(count) ]
	for i in range (0,count):
		row[i] = dataslines[i].split()
	ascii_array = copy.deepcopy(np.array(row)) #深拷贝row给ASCII输出
	if reversebool is False:
		for i in range(len(row)):
			for j in range(len(row[i])):
				if row[i][j] == '1' or row[i][j] == '2':
					row[i][j] = True
				else:
					row[i][j] = False
	else:
		for i in range(len(row)):
			for j in range(len(row[i])):
				if row[i][j] == '1' or row[i][j] == '2':
					row[i][j] = False
				else:
					row[i][j] = True
	bool_array = np.array(row) #储存row为bool
	return bool_array,ascii_array

def reshapearray(data,x,y,z):

	arrayreshaped = data.reshape(x,y,z) #reshape data to 3-dimentional array
	return arrayreshaped

def writedata(data,filenames,x,y,z):
	
	data = data.reshape(x*z,y) #reshape data to 2-dimention for palabos
	localtime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) 
	with open(filenames+'_'+localtime+".dat","a") as f:  
		for i in range(len(data)):
			for j in range(len(data[i])):
				f.write(data[i,j])
				f.write(' ')
			f.write('\n')

def savematfile(data,filenames,key='testvol'):
	'''
	Save data in mat format as 'filenames.mat'.
    Parameters
    ----------
	data : numpy array
	filenames : str
	key : str, set as 'testvol' for matlab program to read
	'''
	scipy.io.savemat(filenames+'.mat',{key:data}) 

if __name__ == "__main__" :

	x,y,z=10,10,10
	#x=y=z=315
	filename = '1'
	binorigin,origin = datreader(filename+'.dat',True)
	writedata(origin,filename+'_reshape',x,y,z)
	savematfile(reshapearray(binorigin,x,y,z),filename)