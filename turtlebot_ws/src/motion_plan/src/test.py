#!/usr/bin/env python


import rospy
import math
import tf

# pub
from geometry_msgs.msg import Twist

# sub
from geometry_msgs.msg import PoseStamped
from motion_plan.msg import reference_point
# sub
# -map
from nav_msgs.msg import OccupancyGrid

# sub_function(get target pose(reference point))
rx=0
ry=0
rt=0
mode=0
def refpoint(data):
    global rx,ry,rt,mode
    rx=data.x
    ry=data.y
    rt=data.theta
    mode=data.mode


# sub function
# sub map data
m_d=[]
def getmap(data):
    global m_d
    m_d=data.data
    m_d=list(m_d)


def pid_Controller():
    rospy.init_node('pid_Controller', anonymous=True)
    rospy.Subscriber('/reference_point',reference_point , refpoint)
    rospy.Subscriber('map', OccupancyGrid, getmap)

    pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
    
    rate = rospy.Rate(1)
    print('start!')
    path = []
    while True:
        if path ==[]:
            i=0
            path.append(i)
        else
            i++
        
    while not rospy.is_shutdown():
        #print ("x",rx,"y",ry,"theta",rt,"mode",mode)
        if len(m_d)!=0:
            #print "m_d100:",[i for i, e in enumerate(m_d) if e==100]
            print "m_d:", m_d[2098196]
        break
if __name__=='__main__':
    try:
        pid_Controller()
    except rospy.ROSInterruptException:
        pass
