#!/usr/bin/env python


import rospy
import math
import tf

# pub
from motion_plan.msg import reference_point

# sub
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float64MultiArray

# sub_function(get trajectory)
traj=[]
def gettraj(data):
    global traj
    traj = data.data
    traj = list(traj)

# sub_function(get hector slam pose)
px=0
py=0
pz=0
qx=0
qy=0
qz=0
qw=0
yaw=0.0
def slamPose(data):
    global px,py,qx,qy,qz,qw,yaw
    px=round(data.pose.position.x,3)
    py=round(data.pose.position.y,3)
    pz=data.pose.position.z
    qx=data.pose.orientation.x
    qy=data.pose.orientation.y
    qz=data.pose.orientation.z
    qw=data.pose.orientation.w
    quaternion = (qx,qy,qz,qw)
    euler = tf.transformations.euler_from_quaternion(quaternion)
    yaw = math.degrees(round(euler[2],3))

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


def path_planner():
    rospy.init_node('PathPlanner_node', anonymous=True)
    rospy.Subscriber('/trajectory',Float64MultiArray , gettraj)
    rospy.Subscriber('slam_out_pose', PoseStamped, slamPose)
    rospy.Subscriber('/target_pose',reference_point , refpoint)
    pub = rospy.Publisher('/reference_point',reference_point, queue_size=10)
    rate = rospy.Rate(1)
    print('start!')

    while not rospy.is_shutdown():
        while True:
            if traj!=[]:
                print traj
                break
        
        i=0
        x_list = []
        y_list = []
        while True:
            x_list.append(traj[i])
            y_list.append(traj[i+1])
            j = len(traj)-2
            if i == j:
                break
            i+=2
        counter=0
        while True:
            r_point = reference_point()
            r_point.x=x_list[counter]
            r_point.y=y_list[counter]
            r_point.theta=rt
            r_point.mode=0
            error_d = math.sqrt((px-x_list[counter])**2+(py-y_list[counter])**2)
            print r_point
            pub.publish(r_point)
            rate.sleep()
            print "publish!!"
            if error_d<0.05:
                done = len(x_list)-1
                if counter==done:
                    print "DONE!!!"                    
                    break
                counter+=1
            
        #print traj






if __name__=='__main__':
    try:
        path_planner()
    except rospy.ROSInterruptException:
        pass


    
