import numpy as np
import two_d_fracture
import porespy as ps

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

def combine(image_array,frac_points):
    """
    docstring
    """
    p0 = (frac_points[0][0],frac_points[1][0])
    p1 = (frac_points[0][1],frac_points[1][1])
    p2 = (frac_points[0][2],frac_points[1][2])
    p3 = (frac_points[0][3],frac_points[1][3])
    for i in range(len(image_array)):
        for j in range(len(image_array[i])):
            p = (i,j)
            if getcorss(p0,p1,p)*getcorss(p2,p3,p) >= 0 and getcorss(p0,p3,p)*getcorss(p2,p1,p) >= 0 :
                image_array[i][j] = 0

    return image_array

def getcorss(p0 :tuple, p1:tuple, p:tuple):
    return (p1[0] - p0[0]) * (p[1] - p0[1]) - (p[0] - p0[0]) * (p1[1] - p0[1])


if __name__ == '__main__':

    image_array = datreader('txt_model\\0.3.txt')
    # im = np.ones((400,300)) #空白模型
    print('初始孔隙度为：',ps.metrics.porosity(image_array))

    fraclist= []
    for _ in range(20): #加入20个随机裂缝，裂缝位置 长宽均随机
       fraclist.append(two_d_fracture.fracture2d([np.random.randint(0, 300),np.random.randint(0, 400)],np.random.randint(5, 10),np.random.randint(50, 60)))
    for i in fraclist:
        i.rotate(np.random.randint(10, 90)) #随机旋转
        image_array = combain(image_array,i.corner_points)
    print('加入随机裂缝后为：',ps.metrics.porosity(image_array))    
    
    image_array.tofile('0.8'+'.raw')