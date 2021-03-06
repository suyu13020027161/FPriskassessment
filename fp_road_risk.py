#苏雨的飞行计划对道路风险检测程序

#######################################################################################################################################################################################################
#苏雨的飞行计划信息提取程序
import csv
with open('flightplan.csv',"r") as csvfile:
    reader = csv.reader(csvfile)
    rows= [row for row in reader]
#print (rows)

#先看一下有几个航班，每个航班几个航点（苏雨）
i = 1
#航班数量（苏雨）
flightnum = 1
#对比名称初始化（苏雨）
name = rows[1][1]
#print (name)
while i < len(rows):
    if rows[i][1] != name:
        flightnum = flightnum + 1
        name = rows[i][1]
    i = i + 1
#print(flightnum)    

#定义二维数组，航班序号，经纬高度速度（苏雨）
flightlat = [[] for j in range(flightnum)]
flightlon = [[] for j in range(flightnum)]
flightalt = [[] for j in range(flightnum)]

i = 1
flightnum = 1
name = rows[1][1]
while i < len(rows):
    if rows[i][1] != name:
        flightnum = flightnum + 1
        name = rows[i][1] 
    flightlat[flightnum-1].append(float(rows[i][3]))
    flightlon[flightnum-1].append(float(rows[i][4]))
    flightalt[flightnum-1].append(float(rows[i][5]))        
    i = i + 1
#print(flightlat) 
#print(flightlon) 
#print(flightalt)
#飞行速度（苏雨）
flspeed = rows[1][7]
#print(flspeed)
#######################################################################################################################################################################################################














#######################################################################################################################################################################################################
#苏雨的道路信息提取程序
# -*- coding: utf-8 -*-
from xml.dom import minidom
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re
import math
from numpy import sqrt
pi = math.pi


#要读取的kml文件名（苏雨）
tree = ET.parse('test2.kml')
root = tree.getroot()
    
namespace = re.match('\{(.*?)\}kml', root.tag).group(1)
ns = {'def': namespace}
    
coord_ex = '(-?\d+\.\d+),'
heig_ex = '(\d+)'
regex = coord_ex + coord_ex + heig_ex

namelist = []
for i in root.findall('.//def:Placemark', ns):
    name = i.find('def:name', ns).text
    #print(name)
    namelist.append(name)

#print(namelist)
#print(len(namelist))


#创建列表存储最大速度（苏雨）
maxspeedlist = []
#提取道路限速（苏雨）
dom=minidom.parse("/home/suyu/FPriskassessment/test2.kml") 
root = dom.documentElement
Placemark = root.getElementsByTagName('Placemark')
listnum = 0
while listnum < len(namelist):
    for i in range(len(Placemark)):
        n = Placemark[i].childNodes[1]
        na = n.firstChild
        name = na.data
        
        #当查到对应的道路名字（苏雨）
        if name == namelist[listnum]:
            #print (name)
            ExtendedData = Placemark[i].childNodes[3] 
           
            #下面请注意，每一条路参数里面限速所在位置都不一样，所以需要动用循环来找（苏雨）
            num = 1    
            while num < len(ExtendedData.childNodes):
                data = ExtendedData.childNodes[num]
                dataname = data.getAttribute("name")
                #print(dataname)
                num = num + 2
                if dataname == 'maxspeed':
                    maxspeed = data.childNodes[1]
                    maxspeedvalue = maxspeed.childNodes[0]
                    maxspeedvalue = maxspeedvalue.data
                    #print(maxspeedvalue)
                    #将限速转换为数值（苏雨）
                    if maxspeedvalue == '70 mph':
                        maxspeedvalue = 70
                        #print(maxspeedvalue)
                        maxspeedlist.append(maxspeedvalue)
                    elif maxspeedvalue == '60 mph':
                        maxspeedvalue = 60
                        #print(maxspeedvalue)
                        maxspeedlist.append(maxspeedvalue)                    
                    elif maxspeedvalue == '40 mph':
                        maxspeedvalue = 40
                        #print(maxspeedvalue)
                        maxspeedlist.append(maxspeedvalue)
                    elif maxspeedvalue == '30 mph':
                        maxspeedvalue = 30
                        #print(maxspeedvalue)
                        maxspeedlist.append(maxspeedvalue)
                    elif maxspeedvalue == '20 mph':
                        maxspeedvalue = 20
                        #print(maxspeedvalue)
                        maxspeedlist.append(maxspeedvalue)                                                                      
            break
    listnum = listnum + 1

#print(maxspeedlist)
#print(len(maxspeedlist))   



#提取道路数据存入二维列表（苏雨）
tree = ET.parse('test2.kml')
root = tree.getroot()   
namespace = re.match('\{(.*?)\}kml', root.tag).group(1)
ns = {'def': namespace}

#注意这里要创建二维列表来存储道路数据（苏雨）
kmllist = [[] for i in range(len(maxspeedlist))]
road_number = 0

          
for i in root.findall('.//def:Placemark', ns):
    name = i.find('def:name', ns).text
    coord = i.find('.//def:coordinates', ns)  
    #按照路的名称，将路的航点分别筛选储存（苏雨）     
    if not coord is None:    
        coord = coord.text.strip()
        coord = re.findall(regex, coord)                                
    #print(count)

    #print(name)
        
    #kmllist = []
    for (long, lat, heig) in coord:
        if i.find('.//def:LineString', ns):                         
            fllong = float(long)
            fllat = float(lat)              
            kmllist[road_number].append(fllong)
            kmllist[road_number].append(fllat) 
    road_number = road_number + 1
#print(kmllist)
#print(len(kmllist))
#######################################################################################################################################################################################################


 



















#######################################################################################################################################################################################################
#苏雨的判断线段是否相交程序
class Point:
    def get(self,text,x,y):
        self.text=text
        self.x = x
        self.y = y       
             

def liesOnSegment(p, q, r):
    if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and 
           (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False
  
def checkOrientation(p, q, r):      
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if (val > 0):
        return 1
    elif (val < 0):
        return 2
    else:
        return 0

def checkIntersection(p1,q1,p2,q2):
    global intersectionresult
    global proper
    o1 = checkOrientation(p1, q1, p2)
    o2 = checkOrientation(p1, q1, q2)
    o3 = checkOrientation(p2, q2, p1)
    o4 = checkOrientation(p2, q2, q1)
    if ((o1 != o2) and (o3 != o4)):
        if(o1==0 or o2==0 or o3==0 or o4==0):
            intersectionresult=True
            proper=False
        else:
            intersectionresult=True
            proper=True
        return True
    if ((o1 == 0) and liesOnSegment(p1, p2, q1)):
        intersectionresult=True
        proper=False
        return True
    if ((o2 == 0) and liesOnSegment(p1, q2, q1)):
        intersectionresult=True
        proper=False
        return True
    if ((o3 == 0) and liesOnSegment(p2, p1, q2)):
        intersectionresult=True
        proper=False
        return True
    if ((o4 == 0) and liesOnSegment(p2, q1, q2)):
        intersectionresult=True
        proper=False
        return True

    intersectionresult=False
    proper=None
    return False
#######################################################################################################################################################################################################














#######################################################################################################################################################################################################
#苏雨的飞行计划和道路相交评估程序
p1=Point()
q1=Point()
p2=Point()
q2=Point()
#请注意，p1,q1是一条线；p2,q2是另一条线（苏雨）
pointlist=[p1,q1,p2,q2]
#定义一个二维向量，把有相交的部分的colist扔进去（苏雨）
problem = []
#定义出现问题航段高度向量（苏雨）
problemh = []
#定义出现问题的道路限速向量（苏雨）
problemrspeed = []
i = 0
while i < (flightnum):
    j = 0
    while j < (len(flightlat[i]) - 1):
        #这里就对每个航线段开始循环判断是否与道路冲突了（苏雨）
        roadnum = 0
        while roadnum < len(kmllist):
            coordnum = 0
            while coordnum < (len(kmllist[roadnum]) - 3):
                #请将需要判断的上述四个顶点xy坐标按顺序存在下面的数组里（苏雨）
                #lat和lon的顺序一定要注意！（苏雨）
                colist = []
                colist.append(flightlon[i][j])
                colist.append(flightlat[i][j])
                colist.append(flightlon[i][j+1])
                colist.append(flightlat[i][j+1])
                colist.append(kmllist[roadnum][coordnum])
                colist.append(kmllist[roadnum][coordnum+1])
                colist.append(kmllist[roadnum][coordnum+2])
                colist.append(kmllist[roadnum][coordnum+3])
                ic = 0
                for p in pointlist:
                    pointname=[key for key,value in locals().items() if value==p]
                    p.get(str(pointname[0]),colist[ic],colist[ic+1])
                    ic = ic + 2
                checkIntersection(p1, q1, p2, q2)
                if(intersectionresult==True):
                    riskarea = [[flightlon[i][j],flightlat[i][j]],[flightlon[i][j+1],flightlat[i][j+1]]]
                    #计算出现问题航段的平均高度（苏雨）
                    avgh = (flightalt[i][j]+flightalt[i][j+1])/2
                    problemh.append(avgh)  
                    problem.append(colist)
                    problemrspeed.append(maxspeedlist[roadnum])
                    #print(riskarea)
                    #print(colist)
                    #print (j)
                    #print (i)
                    #print ('\n')                    
                #else:
                    #print("NO!")   
                coordnum = coordnum + 2
            roadnum = roadnum + 1       
        j = j + 1
    i = i + 1
#print(len(problem))  
#print(len(problemh)) 
#print(len(problemrspeed))  
######################################################################################################################################################################################################
















######################################################################################################################################################################################################
#苏雨的飞行计划风险评估程序
import numpy as np
import time
from shapely.geometry import Polygon  # 多边形
import scipy.io as io

#以旋翼飞行器为例（苏雨）
m = 1.4
v_cruise = float(flspeed)
g = 9.8
row = 1.29
CD = 0.45
A = 0.02
H = 50
#道路风险权重（苏雨）
wroad = 0.3
#道路车辆密度，初步定义为辆每平方米（苏雨）
rowcar = 0.2  

#先求出现问题部分重叠区域面积（苏雨）
#定义重叠区域面积向量（苏雨）
problemarea = []
#定义问题航段风险宽度列表（苏雨）
problemlthreat = []
#求出现问题航段的风险宽度（苏雨）
i = 0
while i < len(problemh):
    Lthreat = v_cruise*sqrt((2*m)/(row*CD*A*g))*math.acosh(math.exp((row*CD*A*float(problemh[i]))/(2*m)))
    problemlthreat.append(Lthreat)
    i = i + 1
#print(problemlthreat)
#print(problem) 

i = 0
#定义最后输出的问题航段坐标向量（苏雨）
reportprob = []
#定义最后输出的问题航段对应的风险值向量（苏雨）
reportrisk = []

while i < len(problem):
    #先把航线和道路相交的两个线段拓展为两个矩形（苏雨）
    #航线矩形（苏雨）
    wpx1 = problem[i][0]
    wpy1 = problem[i][1]
    wpx2 = problem[i][2]
    wpy2 = problem[i][3]
    Length1 = problemlthreat[i]
    H1 = (Length1*(wpx2-wpx1))/(((wpx2-wpx1)**2+(wpy2-wpy1)**2)** 0.5) 
    L1 = (Length1*(wpy2-wpy1))/(((wpx2-wpx1)**2+(wpy2-wpy1)**2)** 0.5)
    #矩形顺时针从左上顶点开始（苏雨）
    #请注意经纬度和米的换算！！！（苏雨）
    latlontom = 180/(pi*111000)                                
    x1 = wpx1 - L1*latlontom
    y1 = wpy1 + H1*latlontom
    x2 = wpx2 - L1*latlontom
    y2 = wpy2 + H1*latlontom
    x3 = wpx2 + L1*latlontom
    y3 = wpy2 - H1*latlontom
    x4 = wpx1 + L1*latlontom
    y4 = wpy1 - H1*latlontom
    #带比较的第一个物体的顶点坐标（苏雨）
    data1 = [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
    #print(data1)

    #道路矩形（苏雨）
    wpx3 = problem[i][4]
    wpy3 = problem[i][5]
    wpx4 = problem[i][6]
    wpy4 = problem[i][7]
    #道路一边宽度为3.5米（苏雨）
    Length2 = 3.5
    H2 = (Length2*(wpx4-wpx3))/(((wpx4-wpx3)**2+(wpy4-wpy3)**2)** 0.5) 
    L2 = (Length1*(wpy4-wpy3))/(((wpx4-wpx3)**2+(wpy4-wpy3)**2)** 0.5)
    #矩形顺时针从左上顶点开始（苏雨）
    x5 = wpx3 - L2*latlontom
    y5 = wpy3 + H2*latlontom
    x6 = wpx4 - L2*latlontom
    y6 = wpy4 + H2*latlontom
    x7 = wpx4 + L2*latlontom
    y7 = wpy4 - H2*latlontom
    x8 = wpx3 + L2*latlontom
    y8 = wpy3 - H2*latlontom
    #带比较的第二个物体的顶点坐标（苏雨）
    data2 = [[x5,y5],[x6,y6],[x7,y7],[x8,y8]]    
    poly1 = Polygon(data1).convex_hull
    poly2 = Polygon(data2).convex_hull
    inter_area = poly1.intersection(poly2).area*(latlontom**(-2))
    problemarea.append(inter_area)
    i = i + 1    
#print(problem)    
#现在飞行计划风险区域和道路相交部分的面积就求出来了（苏雨）









#计算道路风险（苏雨）
#坠落概率（苏雨）
P_crash = 1/10**3

#最终道路风险航段坐标向量（苏雨）
problematicroadplan = []
#最终道路风险航段对应的风险（苏雨）
problematicroadrisk = []

i = 0
j = 0
#定义航段比较参数并初始化（苏雨）
compare = [problem[0][0],problem[0][1],problem[0][2],problem[0][3]]
while i < len(problem):
    #如果是第一位直接算风险存入向量第一位（苏雨）
    if i == 0:
        #开始计算风险（苏雨）    
        #P_impact和受影响车辆数量线性相关，系数暂定为1（苏雨）
        P_impact = problemarea[i]*rowcar
        #冲击动能（苏雨）
        Ek = (m*(v_cruise+problemrspeed[i])**2)/2 + ((m**2*g)/(row*CD*A))*(1-math.exp(-(row*CD*A*H)/m))
        P_fatality = 1/(1+100*(100/Ek)**0.5)
        #最终航段道路风险（苏雨）
        Rroad = wroad*P_crash*P_impact*P_fatality*10**5
        problematicroadrisk.append(Rroad)
        problematicroadplan.append([problem[0][0],problem[0][1],problem[0][2],problem[0][3]])
    else:
        #如果是同一条航段（苏雨）
        if compare == [problem[i][0],problem[i][1],problem[i][2],problem[i][3]]:
            P_impact = problemarea[i]*rowcar
            Ek = (m*(v_cruise+problemrspeed[i])**2)/2 + ((m**2*g)/(row*CD*A))*(1-math.exp(-(row*CD*A*H)/m))   
            P_fatality = 1/(1+100*(100/Ek)**0.5)
            #风险为了便于对比，乘10^5（苏雨）
            Rroad = wroad*P_crash*P_impact*P_fatality*10**5
            #同航段风险直接往上加（苏雨）
            problematicroadrisk[j] = problematicroadrisk[j] + Rroad
        #如果不是同一条航段（苏雨）
        else:
            j = j + 1
            P_impact = problemarea[i]*rowcar
            Ek = (m*(v_cruise+problemrspeed[i])**2)/2 + ((m**2*g)/(row*CD*A))*(1-math.exp(-(row*CD*A*H)/m))   
            P_fatality = 1/(1+100*(100/Ek)**0.5)
            Rroad = wroad*P_crash*P_impact*P_fatality*10**5
            #同航段风险直接往上加（苏雨）
            problematicroadrisk.append(Rroad)
            problematicroadplan.append([problem[i][0],problem[i][1],problem[i][2],problem[i][3]])
            compare = [problem[i][0],problem[i][1],problem[i][2],problem[i][3]]            
    i = i + 1

print(problematicroadplan)
print(problematicroadrisk)













  




















######################################################################################################################################################################################################





