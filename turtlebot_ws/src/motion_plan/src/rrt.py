#!/usr/bin/env python

import rospy
import math
import tf
import random

# pub
# -trajectory
from std_msgs.msg import Float64MultiArray

# sub
# -map
from nav_msgs.msg import OccupancyGrid
# -slam_out_pose
from geometry_msgs.msg import PoseStamped
# -target_pose
from motion_plan.msg import reference_point

# Constant
THRESHOLD=0.05*2
THRESHOLD_TARGET=0.08

# global var
used_list=[]
TREE = []

# sub function
# sub map data
m_d=[]
def getmap(data):
    global m_d
    m_d=data.data
    m_d=list(m_d)

# sub slam_out_pose data
px=0
py=0
qx=0
qy=0
qz=0
qw=0
yaw=0.0
def slamPose(data):
    global px,py,qx,qy,qz,qw,yaw
    px=data.pose.position.x
    py=data.pose.position.y
    pz=data.pose.position.z
    qx=data.pose.orientation.x
    qy=data.pose.orientation.y
    qz=data.pose.orientation.z
    qw=data.pose.orientation.w
    quaternion = (qx,qy,qz,qw)
    euler = tf.transformations.euler_from_quaternion(quaternion)
    yaw = euler[2]


# sub_function(get target pose)
rx=0
ry=0
rt=0
mode=2
def refpoint(data):
    global rx,ry,rt,mode
    rx=data.x
    ry=data.y
    rt=data.theta
    mode=data.mode
    #print "here"


# other function
def distance(cx,cy,tx,ty):
    dis = math.sqrt((tx-cx)**2+(ty-cy)**2)
    return dis
    

# necessary function
#used=[]
def random_configuration(config_list):
    #print "find a random point"
    #print len(config_list)
    
    config_point=random.choice(config_list)
    tx =config_point%2048
    ty =config_point//2048
    tx =(tx-1024)*0.05
    ty =(ty-1024)*0.05     
    return tx,ty
    #print "now",len(config_list) ans:1005

    

def nearest_vertex(tx,ty):
    #print "find a nearest_vertex"
    shortest_d = 0
    for node in TREE:
        x=node[1][0]
        y=node[1][1]
        temp_d = distance(x,y,tx,ty)
        if shortest_d<temp_d:
            shortest_d=temp_d
    #print "d:", shortest_d
    for node in TREE:
        x=node[1][0]
        y=node[1][1]
        if distance(x,y,tx,ty)==shortest_d:
            near_node = node
            return near_node

def new_configuration(near_node,tx,ty):
    #print "choose new node"
    nx=near_node[1][0]
    ny=near_node[1][1]
    ideal_x=0
    ideal_y=0
    if tx==nx:
        d= distance(nx,ny,tx,ty)
        if d<THRESHOLD:
            new_node=[tx,ty]
        else:
            ideal_x=nx
            ideal_y=ny+THRESHOLD
    else:
        d= distance(nx,ny,tx,ty)
        theta = math.atan2(ty-ny,tx-nx)
        m=(ty-ny)/(tx-nx)
        b=ty-(m*tx)
        if d<THRESHOLD:
            new_node=[tx,ty]
        else:
            ideal_x = THRESHOLD*math.cos(theta)
            ideal_y = ideal_x*m+b
            
    new_node=[ideal_x,ideal_y] 
    return new_node

def add_vertex(near_node,new_node):
    #add new_node to tree
    
    #print "add node to tree"
    global TREE
    i=0
    parent = 0
    for node in TREE:
        
        if node[1]==near_node[1]:
            parent = i
              
        i+=1
    
    data = new_node
    children = []

    #print "here"
    TREE.append([parent,data,children])
    j=len(TREE)-1
    TREE[parent][2].append(j)    


# main function
def rrt():
    global TREE
    rospy.init_node('RRT_node', anonymous=True)
    rospy.Subscriber('slam_out_pose', PoseStamped, slamPose)
    rospy.Subscriber('/target_pose',reference_point , refpoint)
    rospy.Subscriber('map', OccupancyGrid, getmap)
    pub = rospy.Publisher('/trajectory',Float64MultiArray, queue_size=10)
    rate = rospy.Rate(1)
    print('start!')
    while not rospy.is_shutdown():
        while True:
            if len(m_d)==4194304:
                break
        point_list=[i for i, e in enumerate(m_d) if e==0]
        obs_list = [a for a, b in enumerate(m_d) if b==100]
        #transform to configuration space
        config_list=[]
        for point in point_list:
            counter=0
            for item in obs_list:
                #print "ya:",point
                x =point%2048
                y =point//2048
                x =(x-1024)*0.05
                y =(y-1024)*0.05
                ox =item%2048
                oy =item//2048
                ox =(ox-1024)*0.05
                oy =(oy-1024)*0.05
                d = distance(x,y,ox,oy)
                if d>0.5:
                    counter+=1
                    if counter==len(obs_list):
                        config_list.append(point)
        #print "map has config",len(config_list)
        #print config_list
        
        
        counter=0
        
        while len(m_d)==4194304:
            
            if TREE == []:
                TREE.append([[],[px,py],[]])
            else:
                while True:
                    x,y=random_configuration(config_list)
                    near_node=nearest_vertex(x,y)
                    new_node=new_configuration(near_node,x,y)
                    add_vertex(near_node,new_node)
                    target_error=distance(new_node[0],new_node[1],rx,ry)
                    if target_error < THRESHOLD_TARGET:
                        print "get point "
                        break
                print "hihihhi"
                path = [TREE[-1][1]]
                prev_node = TREE[-1][0]
                while True:
                    path.append(TREE[prev_node][1])
                    prev_node=TREE[prev_node][0]
                    if prev_node==[]:
                        break
                path.reverse()
                path = [j for sub in path for j in sub]
                while True:
                    traj = Float64MultiArray()
                    traj.data = path
                    pub.publish(traj)
                    rate.sleep()
                    if distance(px,py,path[-2],path[-1])<0.05:
                        TREE=[]
                        break
            print "wait!!"    
           
        #path = []
    
        #while True:
            
        
            
        #break#shutdown node
            
        

if __name__=='__main__':
    try:
        rrt()
    except rospy.ROSInterruptException:
        pass






