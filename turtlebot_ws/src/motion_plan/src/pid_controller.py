#!/usr/bin/env python


import rospy
import math
import tf

# pub
from geometry_msgs.msg import Twist

# sub
from geometry_msgs.msg import PoseStamped
from motion_plan.msg import reference_point


#tuning constant
Kp=0.005
Kd=0.00001
Ki=0.0001
THRESHOLD_ANG=0.5
THRESHOLD_LIN=0.05

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

# sub_function(get target pose(reference point))
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
    
# other function
'''
# xc: current x position
# yc: current y position
# tc: current theta position
# xg: goal x position
# yg: goal y position
# tg: goal theta position
# return: 
# linear error: error_lin
# angular error from current to goal: error_ang_d
# angular error from goal to goal: error_ang_g
'''
def pid_error(xc,yc,tc,xg,yg,tg):
    error_lin = math.sqrt((xg-xc)**2+(yg-yc)**2)
    error_ang_d = math.degrees(math.atan2((yg-yc),(xg-xc)))-tc
    error_ang_g = tg-tc
    return error_lin,error_ang_d,error_ang_g
	
# node and pub function
def pid_Controller():
    rospy.init_node('pid_Controller', anonymous=True)
    rospy.Subscriber('slam_out_pose', PoseStamped, slamPose)
    rospy.Subscriber('/reference_point',reference_point , refpoint)
    pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
    rate = rospy.Rate(1)
    print('start!')
   
    
    while not rospy.is_shutdown():
        if mode!=2:
            move_cmd=Twist()
            if rt>180 or rt<-180:
                print('The theta can only be -180~180')
                break
            if mode==0:
                print "mode0 go!!"
                #counter=0
                error_lin=0
                error_ang=0
                prev_lin=0
                prev_ang=0
                int_lin=0
                int_ang=0
                print "rotate to target direction"
                while True:
                    #step 1
                    error_lin,error_ang_d,error_ang_g=pid_error(px,py,yaw,rx,ry,rt)
                    move_cmd.linear.x=0
                    error_ang = error_ang_d
                    move_cmd.angular.z=Kp*error_ang+Ki*(error_ang-prev_ang)+Kd*(int_ang)
                    pub.publish(move_cmd)
                    #print error_ang_d
                    prev_ang=error_ang
                    int_ang+=error_ang
                    rate.sleep()
                    if abs(error_ang_d)<THRESHOLD_ANG:
                        break
                print "go to the target position"
                while True:      
                    #step2
                    error_lin,error_ang_d,error_ang_g=pid_error(px,py,yaw,rx,ry,rt)
                    move_cmd.linear.x=15*(Kp*error_lin+Ki*(error_lin-prev_lin)+Kd*(int_lin))
                    move_cmd.angular.z=0
                    pub.publish(move_cmd)
                    #print error_lin
                    prev_lin=error_lin
                    int_lin+=error_lin
                    rate.sleep()
                    if abs(error_ang_d)>THRESHOLD_ANG:
                        print "path correction!"
                        while True:
                            #step 1
                            error_lin,error_ang_d,error_ang_g=pid_error(px,py,yaw,rx,ry,rt)
                            move_cmd.linear.x=0
                            error_ang = error_ang_d
                            move_cmd.angular.z=Kp*error_ang+Ki*(error_ang-prev_ang)+Kd*(int_ang)
                            pub.publish(move_cmd)
                            #print error_ang_d
                            prev_ang=error_ang
                            int_ang+=error_ang
                            rate.sleep()
                            if abs(error_ang_d)<THRESHOLD_ANG:
                                break
                    if error_lin<THRESHOLD_LIN:
                        break
                print "rotate to ideal pose"
                while True:
                    #step3
                    error_lin,error_ang_d,error_ang_g=pid_error(px,py,yaw,rx,ry,rt)
                    move_cmd.linear.x=0
                    error_ang = error_ang_g
                    move_cmd.angular.z=Kp*error_ang+Ki*(error_ang-prev_ang)+Kd*(int_ang)
                    pub.publish(move_cmd)
                    #print error_ang_g
                    prev_ang=error_ang
                    int_ang+=error_ang
                    rate.sleep()
                    #counter+=1
                    if abs(error_ang_g)<THRESHOLD_ANG:
                        print "finish"
                        print "wait for new point"
                        while True:
                            print "wait"
                            error_lin,error_ang_d,error_ang_g=pid_error(px,py,yaw,rx,ry,rt)
                            move_cmd.linear.x=0    
                            move_cmd.angular.z=0
                            pub.publish(move_cmd)
                            if error_lin>THRESHOLD_LIN:
                                break
                        break
                
   
            elif mode==1:
                print "mode1 go!!"
                error_lin=0
                error_ang=0
                prev_lin=0
                prev_ang=0
                int_lin=0
                int_ang=0
                while True:
                    error_lin,error_ang_d,error_ang_g=pid_error(px,py,yaw,rx,ry,rt)
                    move_cmd.linear.x=15*(Kp*error_lin+Ki*(error_lin-prev_lin)+Kd*(int_lin))
                    move_cmd.angular.z=Kp*error_ang_d+Ki*(error_ang_d-prev_ang)+Kd*(int_ang)
                    pub.publish(move_cmd)
                    prev_lin=error_lin
                    prev_ang=error_ang_d
                    int_lin+=error_lin
                    int_ang+=error_ang_d
                    rate.sleep()
                    if error_lin<THRESHOLD_LIN:
                        prev_ang=0
                        int_ang=0
                        print "rotate to ideal target pose"
                        while True:
                            error_lin,error_ang_d,error_ang_g=pid_error(px,py,yaw,rx,ry,rt)
                            move_cmd.linear.x=0
                            move_cmd.angular.z=Kp*error_ang_g+Ki*(error_ang_g-prev_ang)+Kd*(int_ang)
                            pub.publish(move_cmd)
                            prev_ang=error_ang_g
                            int_ang+=error_ang_g
                            rate.sleep()
                            if abs(error_ang_g)<THRESHOLD_ANG:
                                print "finish"
                                print "wait for new point"
                                while True:
                                    print "wait"
                                    error_lin,error_ang_d,error_ang_g=pid_error(px,py,yaw,rx,ry,rt)
                                    move_cmd.linear.x=0    
                                    move_cmd.angular.z=0
                                    pub.publish(move_cmd)
                                    if error_lin>THRESHOLD_LIN:
                                        break
                                break
                        break
            else:
                print('The mode can only be 0 or 1')
                
        else:
            print('The mode can only be 0 or 1')
if __name__=='__main__':
    try:
        pid_Controller()
    except rospy.ROSInterruptException:
        pass

