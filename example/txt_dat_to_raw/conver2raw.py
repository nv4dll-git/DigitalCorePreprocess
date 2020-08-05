#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2020 JIA Haowei, SWPU
E-mail : nv4dll@outlook.com
'''

import numpy as np

def datreader(filename,reversebool=False):
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
    return bool_array

if __name__ == "__main__":
    image_array= datreader('example\\txt_model_sample\\model.txt')
    image_array.tofile('example\\raw_output\\newdata.raw')
