import numpy as np  
import math
import matplotlib.pyplot as plt

class fracture3d():

    def __init__(self,middle_point:list,frac_width,frac_length,frac_higth):
        self.middle_point = middle_point #裂缝中点坐标
        self.points_num = 8 #角点数
        #矩形从右上角开始沿顺时针方向依次为点0、1、2、3，第二层为 4、5、6、7
        self.corner_points=[[self.middle_point[0] + frac_length/2, self.middle_point[0] + frac_length/2,
                            self.middle_point[0] - frac_length/2,  self.middle_point[0] - frac_length/2,
                            self.middle_point[0] + frac_length/2, self.middle_point[0] + frac_length/2,
                            self.middle_point[0] - frac_length/2,  self.middle_point[0] - frac_length/2],
                            [self.middle_point[1] + frac_width/2, self.middle_point[1] - frac_width/2,
                            self.middle_point[1] - frac_width/2, self.middle_point[1] + frac_width/2,
                            self.middle_point[1] + frac_width/2, self.middle_point[1] - frac_width/2,
                            self.middle_point[1] - frac_width/2, self.middle_point[1] + frac_width/2],
                            [self.middle_point[2] + frac_higth/2, self.middle_point[2] + frac_higth/2,
                            self.middle_point[2] + frac_higth/2, self.middle_point[2] + frac_higth/2,
                            self.middle_point[2] - frac_higth/2, self.middle_point[2] - frac_higth/2,
                            self.middle_point[2] - frac_higth/2, self.middle_point[2] - frac_higth/2
                            ]]
        self.frac_width = frac_width #裂缝宽
        self.frac_length = frac_length #裂缝长
        self.frac_higth = frac_higth #裂缝高
        self.rotate_count = 0 #旋转计数
        self._build_frac()

    def _build_frac(self):
        #由生成线
        line1_y = np.arange(self.corner_points[1][1],self.corner_points[0][1]-1,1) #从矩形右上角开始构建，点数量为长度加1
        line1_x = np.full((len(line1_y)),self.corner_points[0][0])
        line1_z = np.full((len(line1_y)),self.corner_points[2][0])

        face1_x = [] #由线生成面
        face1_y = []
        face1_z = []

        for _ in range(self.frac_length+1): #建立第一个面
            if _ == 0 :
                face1_x = np.concatenate((face1_x,line1_x)) #第一列x相等
            else:
                face1_x = np.concatenate((face1_x,line1_x - _))#x坐标依次减小
            face1_y = np.concatenate((face1_y,line1_y)) #第一个面的y坐标复制即可
            face1_z = np.concatenate((face1_z,line1_z))#第一个面的z坐标复制即可
        
        face_x = [] 
        face_y = []
        face_z = []
        for _ in range(self.frac_higth): #建立体积 叠加各面

            face_x = np.concatenate((face_x,face1_x))
            face_y = np.concatenate((face_y,face1_y))
            if _ == 0 :
                face_z = np.concatenate((face_z,face1_z))
            else:
                face_z = np.concatenate((face_z,face1_z-_))
        self.volume = np.vstack((face_x,face_y,face_z))
    
    def plot_frac_outline(self):
        
        ax = plt.axes(projection='3d')
        for i in range(self.points_num):
            if i == 7:
                ax.plot3D([self.corner_points[0][i],self.corner_points[0][4]],[self.corner_points[1][i],self.corner_points[1][4]],[self.corner_points[2][i],self.corner_points[2][4]],c='b')
                ax.plot3D([self.corner_points[0][i],self.corner_points[0][3]],[self.corner_points[1][i],self.corner_points[1][3]],[self.corner_points[2][i],self.corner_points[2][3]],c='b')
            elif i == 0:
                ax.plot3D([self.corner_points[0][i],self.corner_points[0][i+1]],[self.corner_points[1][i],self.corner_points[1][i+1]],[self.corner_points[2][i],self.corner_points[2][i+1]],c='b')
                ax.plot3D([self.corner_points[0][i],self.corner_points[0][4]],[self.corner_points[1][i],self.corner_points[1][4]],[self.corner_points[2][i],self.corner_points[2][4]],c='b')
            elif i == 1:  
                ax.plot3D([self.corner_points[0][i],self.corner_points[0][i+1]],[self.corner_points[1][i],self.corner_points[1][i+1]],[self.corner_points[2][i],self.corner_points[2][i+1]],c='b')
                ax.plot3D([self.corner_points[0][i],self.corner_points[0][5]],[self.corner_points[1][i],self.corner_points[1][5]],[self.corner_points[2][i],self.corner_points[2][5]],c='b')
            elif i == 2:  
                ax.plot3D([self.corner_points[0][i],self.corner_points[0][i+1]],[self.corner_points[1][i],self.corner_points[1][i+1]],[self.corner_points[2][i],self.corner_points[2][i+1]],c='b')
                ax.plot3D([self.corner_points[0][i],self.corner_points[0][6]],[self.corner_points[1][i],self.corner_points[1][6]],[self.corner_points[2][i],self.corner_points[2][6]],c='b')
            elif i == 3:
                ax.plot3D([self.corner_points[0][i],self.corner_points[0][0]],[self.corner_points[1][i],self.corner_points[1][0]],[self.corner_points[2][i],self.corner_points[2][0]],c='b')
            else :
                ax.plot3D([self.corner_points[0][i],self.corner_points[0][i+1]],[self.corner_points[1][i],self.corner_points[1][i+1]],[self.corner_points[2][i],self.corner_points[2][i+1]],c='b')
        # ax.plot3D(self.corner_points[0],self.corner_points[1],self.corner_points[2],c='b')
        ax.scatter3D(self.corner_points[0],self.corner_points[1],self.corner_points[2],c='b')
        # plt.show()

    def plot_volume(self):

        ax = plt.axes(projection='3d')
        ax.scatter3D(self.volume[0],self.volume[1],self.volume[2],c='b')
        # plt.show()
        
    def check_shape(self):

        print( 'Rotation:',self.rotate_count)
        print( 'width: ',math.sqrt( (self.corner_points[0][0]-self.corner_points[0][1])**2 + (self.corner_points[1][0]-self.corner_points[1][1])**2 + (self.corner_points[2][0]-self.corner_points[2][1])**2) )
        print( 'length: ',math.sqrt( (self.corner_points[0][1]-self.corner_points[0][2])**2 + (self.corner_points[1][1]-self.corner_points[1][2])**2 + (self.corner_points[2][1]-self.corner_points[2][2])**2) )

    def rotate_xy(self,angle):

        angle = angle*math.pi/180 #弧度转角度
        new_points_x = []
        new_points_y = []

        for i in range(len(self.volume[0])): #以中点为中心 在xy平面旋转
            new_points_x.append((self.volume[0][i] - self.middle_point[0]) * math.cos(angle) - (self.volume[1][i] - self.middle_point[1]) * math.sin(angle) + self.middle_point[0])
            new_points_y.append((self.volume[0][i] - self.middle_point[0]) * math.sin(angle) + (self.volume[1][i] - self.middle_point[1]) * math.cos(angle) + self.middle_point[1])   
        self.volume[0] = new_points_x
        self.volume[1] = new_points_y

        new_corner_points_x = []
        new_corner_points_y = []

        for i in range(self.points_num): #以中点为中心 在xy平面旋转
            new_corner_points_x.append((self.corner_points[0][i] - self.middle_point[0]) * math.cos(angle) - (self.corner_points[1][i] - self.middle_point[1]) * math.sin(angle) + self.middle_point[0])
            new_corner_points_y.append((self.corner_points[0][i] - self.middle_point[0]) * math.sin(angle) + (self.corner_points[1][i] - self.middle_point[1]) * math.cos(angle) + self.middle_point[1])   
        self.corner_points[0]= new_corner_points_x
        self.corner_points[1]= new_corner_points_y

        self.rotate_count += 1
        self.check_shape()
        
    
    def rotate_xz(self,angle):

        angle = angle*math.pi/180 #弧度转角度
        new_points_x = []
        new_points_z = []

        for i in range(len(self.volume[0])): #以中点为中心 在xz平面旋转
            new_points_x.append((self.volume[0][i] - self.middle_point[0]) * math.cos(angle) - (self.volume[2][i] - self.middle_point[2]) * math.sin(angle) + self.middle_point[0])
            new_points_z.append((self.volume[0][i] - self.middle_point[0]) * math.sin(angle) + (self.volume[2][i] - self.middle_point[2]) * math.cos(angle) + self.middle_point[2])   
        self.volume[0]= new_points_x
        self.volume[2]= new_points_z
        
        new_corner_points_x = []
        new_corner_points_y = []

        for i in range(self.points_num): #以中点为中心 在xy平面旋转
            new_corner_points_x.append((self.corner_points[0][i] - self.middle_point[0]) * math.cos(angle) - (self.corner_points[2][i] - self.middle_point[2]) * math.sin(angle) + self.middle_point[0])
            new_corner_points_y.append((self.corner_points[0][i] - self.middle_point[0]) * math.sin(angle) + (self.corner_points[2][i] - self.middle_point[2]) * math.cos(angle) + self.middle_point[2])   
        self.corner_points[0]= new_corner_points_x
        self.corner_points[2]= new_corner_points_y

        self.rotate_count += 1
        self.check_shape()

if __name__ == '__main__':

    frac = fracture3d([1,2,3],5,10,20)
    frac.rotate_xy(30)
    frac.rotate_xz(60)
    frac.plot_volume()
    plt.show()
    # frac.rotate_xz(45)
    # frac.rotate_xy(30)
    # frac.plot_frac()

