import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib import cm
import random
import porespy as ps
#np.random.seed(0) #固定随机数用的 可以注释

def rough_surface(M,N,omega=0.5,kxi=1):
    # omega = 0.5E-6 #高度起伏均方根为0.1064um
    # kxi = 4.75E-6  #横向相干长度为4.75um

    Lx = M*kxi #二维随机粗糙表面x方向长度
    Ly = N*kxi #二维随机粗糙表面y方向长度

    ux = np.arange(-M/2,M/2+1,1) #X方向
    uy = np.arange(-N/2,N/2+1,1) #Y方向
    Ux =2*math.pi*ux/Lx #X方向离散波数
    Uy =2*math.pi*uy/Ly #Y方向离散波数

    vx = np.arange(-M/2,M/2+1,1) #X方向
    vy = np.arange(-N/2,N/2+1,1) #Y方向
    [vx,vy] = np.meshgrid(vx,vy)
    deltax = Lx/M #X方向采样间隔
    deltay = Ly/N #Y方向采样间隔
    Vx = vx*deltax #X方向
    Vy = vy*deltay #Y方向

    ##############################################
    #孔径函数
    P = np.zeros((M+1,N+1),dtype=complex)
    for i in range(M+1):
        for j in range(N+1):    
            P[i][j]=np.sum(np.sum(omega**2*np.exp(-(Vx**2+Vy**2)/(kxi**2))*np.exp(1j*(Ux[i]*Vx+Uy[j]*Vy))*deltax*deltay, axis=0))
    ##############################################
    #复高度分布
    x0 = np.arange(-M/2,M/2+1,1) #X方向
    y0 = np.arange(-N/2,N/2+1,1) #Y方向
    X0 = x0*deltax #X方向
    Y0 = y0*deltay #Y方向
    [Ux0,Uy0] = np.meshgrid(Ux,Uy)

    yita = (np.random.randn(M+1,N+1)+1j*np.random.randn(M+1,N+1))/math.sqrt(2);

    hc = np.zeros((M+1,N+1),dtype=int) #只保留整数，模型最小分辨率为一个像素点
    for i in range(M+1):
        for j in range(N+1):   
            hc[i][j]=np.sqrt(2)*math.pi*np.sum(np.sum(np.sqrt(P)*yita*np.exp(-1j*(Ux0*X0[i]+Uy0*Y0[j])),axis=0))/np.sqrt(Lx*Ly)
    return vx,vy,hc

def empty_box(b_wide,b_long,b_height):
    #生成一个空间
    box = np.zeros((b_wide,b_long,b_height)) #生成孔隙 以0为孔隙空间
    box[:,:,0] = 1 #添加空间底面 1为基质 0为孔隙
    box[:,:,box.shape[2]-1] = 1 #添加空间顶面 1为基质 0为孔隙
    return(box)

def add_rough_surface(box,surface,height_level=0,projection='above'):
    '''
    将粗糙面添加进box中。
    height_level为粗糙面基准高度，projection为投影方向
    '''
    if projection == 'above':
        #'above'为保留粗糙面上面的空间，将box中粗糙面下面的部分设为基质
        surface += height_level
        for i in range(surface.shape[0]):
            for j in range(surface.shape[1]):
                if surface[i,j] < 0: #防止数组越界
                    surface[i,j] = 0
                box[i,j,0:surface[i,j]] = 1       
    elif projection == 'bottom':
        #'bottom'为保留粗糙面下面的空间，将box中粗糙面上面的部分设为基质
        surface += height_level
        for i in range(surface.shape[0]):
            for j in range(surface.shape[1]):
                if surface[i,j] < 0: #防止数组越界
                    surface[i,j] = 0
                box[i,j,surface[i,j]:box.shape[2]+1] = 1
    return box

M = 50 #模型空间x方向大小
N = 50 #模型空间y方向大小 x大小必须等于y大小
hight = 20 #模型高度大小
rough_surface_level_1 = 2 #粗糙面1在空间中基准位置 z方向
rough_surface_level_2 = 18 #粗糙面2在空间中基准位置 z方向

x,y,rc1 = rough_surface(M,N,omega=0.5,kxi=1) #生成下粗糙面
x,y,rc2 = rough_surface(M,N,omega=0.5,kxi=1) #生成上粗糙面
########################## 生成空模型并添加粗糙面
box = empty_box(M+1,N+1,hight)
add_rough_surface(box,rc1,height_level=rough_surface_level_1,projection='above')
add_rough_surface(box,rc2,height_level=rough_surface_level_2,projection='bottom')
########################## 画图部分
fig = plt.figure()
ax1 = fig.gca(projection='3d')
surf1 = ax1.plot_surface(x,y,rc1+rough_surface_level_1, cmap=cm.coolwarm,linewidth=0, antialiased=False)
surf2 = ax1.plot_surface(x,y,rc2+rough_surface_level_2, cmap=cm.coolwarm,linewidth=0, antialiased=False)
# plt.matshow(box[5,:,:], cmap=plt.cm.Blues) #绘制截面

box.tofile('0.7_'+str(box.shape[0])+'_'+str(box.shape[1])+'_'+str(box.shape[2])+'.raw')#输出模型为raw格式

ps.io.to_palabos(box,'demo.dat') #输出为palabos格式
plt.show()