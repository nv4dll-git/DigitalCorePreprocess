from typing import List
import numpy as np
import three_d_fracture
import porespy as ps

def datreader(filename,reversebool:bool=False):
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
                    row[i][j] = 0
                else:
                    row[i][j] = 1
    else:
        for i in range(len(row)):
            for j in range(len(row[i])):
                if row[i][j] == '1' or row[i][j] == '2':
                    row[i][j] = 1
                else:
                    row[i][j] = 0
    bool_array = np.array(row) #储存row为bool
    return bool_array

def combine(im:np.array,im_shape:list,frac_points:three_d_fracture.fracture3d):
    """
    叠加模型
    """
    for i in range(len(frac_points.volume[0])):
        if int(frac_points.volume[0][i]) < 0 or int(frac_points.volume[1][i]) < 0 or int(frac_points.volume[2][i]) < 0 :
            pass
        else:
            #以二维数组储存三维模型，每层依次放置
            dz = (int(frac_points.volume[2][i])-1)*im_shape[2] #z坐标补偿值
            if dz < 0: #检查索引
                dz = 0
            x = int(frac_points.volume[0][i])-1
            if x < 0: #检查索引
                x = 0
            y = int(frac_points.volume[1][i]) + dz  #z坐标补偿值+y坐标为点在列表中实际位置
            if  x > len(im[0]) or y > len(im):
                pass
            else: 
                im[y][x] = 1 #变为孔隙 
    return im


if __name__ == '__main__':

    
    im = datreader('txt_model\\碳酸盐岩2_BinaryData_DigitalCore.txt',reversebool=True)
    print('初始孔隙度为：',ps.metrics.porosity(im))
    
    fraclist= []  #裂缝储存列表高
    for _ in range(20): #加入20个随机裂缝，裂缝位置 长宽均随机
       fraclist.append(three_d_fracture.fracture3d([np.random.randint(5, 20),np.random.randint(5, 20),np.random.randint(5, 20)],np.random.randint(10, 20),np.random.randint(5, 10),np.random.randint(1, 5)))
    for i in fraclist:
        i.rotate_xy(np.random.randint(10, 90)) #随机旋转
        i.rotate_xz(np.random.randint(10, 90)) #随机旋转
        im = combine(im,[30,30,30],i) #叠加模型
    
    # fra = three_d_fracture.fracture3d((15,15,15),10,20,3)
    # im = combine(im,[30,30,30],fra)
    print('加入随机裂缝后为：',ps.metrics.porosity(im))    
    im.tofile('0.9'+'.raw')