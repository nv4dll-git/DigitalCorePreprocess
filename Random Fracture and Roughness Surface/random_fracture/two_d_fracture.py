import numpy as np  
import math
import matplotlib.pyplot as plt

class fracture2d():

    def __init__(self,middle_point:list,frac_width,frac_length):
        self.middle_point = middle_point #裂缝中点坐标
        self.points_num = 4 #角点数
        self.corner_points=[[self.middle_point[0] + frac_length/2, self.middle_point[0] + frac_length/2,
                            self.middle_point[0] - frac_length/2,  self.middle_point[0] - frac_length/2],
                            [self.middle_point[1] + frac_width/2, self.middle_point[1] - frac_width/2,
                            self.middle_point[1] - frac_width/2, self.middle_point[1] + frac_width/2]]
        self.frac_width = frac_width #裂缝宽
        self.frac_length = frac_length #裂缝长

    def rotate(self,angle):

        angle = angle*math.pi/180 #弧度转角度
        new_points_x = []
        new_points_y = []

        for i in range(self.points_num): #以中点为中心 在xy平面旋转
            new_points_x.append((self.corner_points[0][i] - self.middle_point[0]) * math.cos(angle) - (self.corner_points[1][i] - self.middle_point[1]) * math.sin(angle) + self.middle_point[0])
            new_points_y.append((self.corner_points[0][i] - self.middle_point[0]) * math.sin(angle) + (self.corner_points[1][i] - self.middle_point[1]) * math.cos(angle) + self.middle_point[1])   
        self.corner_points[0]= new_points_x
        self.corner_points[1]= new_points_y
        
        # print( 'new width: ',math.sqrt((self.corner_points[0][0]-self.corner_points[0][1])**2 + (self.corner_points[1][0]-self.corner_points[1][1])**2) )
        # print( 'new length: ',math.sqrt((self.corner_points[0][1]-self.corner_points[0][2])**2 + (self.corner_points[1][1]-self.corner_points[1][2])**2) )
        
    def plot_frac(self):
        plt.plot(self.corner_points[0],self.corner_points[1],c='b')
        plt.scatter(self.corner_points[0],self.corner_points[1],c='b')
        plt.show()

if __name__ == '__main__':
    frac = fracture2d([0,0],5,10)
    frac.rotate(30)

