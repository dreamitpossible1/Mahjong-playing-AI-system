#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
from sensor_msgs.msg import Image
import rospy, sys
import moveit_commander
from cv_bridge import CvBridge, CvBridgeError
fix_position = []
for i in range(8):
    fix_position.append([0,0])
fix_position[0][0] = [-0.40,-0.33,-0.645,0,0.38,1.57]
fix_position[0][1] = [-0.4,-0.27,-0.24,0,0.38,1.57]
fix_position[1][0] = [-0.30,-0.37,-0.645,0,0.38,1.57]
fix_position[1][1] = [-0.3,-0.27,-0.14,0,0.38,1.57]
fix_position[2][0] = [-0.20,-0.37,-0.645,0,0.38,1.57]
fix_position[2][1] = [-0.2,-0.27,-0.14,0,0.38,1.57]
fix_position[3][0] = [-0.10,-0.37,-0.645,0,0.38,1.57]
fix_position[3][1] = [-0.1,-0.27,-0.14,0,0.38,1.57]
fix_position[4][0] = [0,-0.32,-0.77,0,0.48,1.57]
fix_position[4][1] = [0,-0.4,-0.5,0,0.48,1.57]
fix_position[5][0] = [0.15,-0.32,-0.77,0,0.48,1.57]
fix_position[5][1] = [0.15,-0.4,-0.5,0,0.48,1.57]
fix_position[6][0] = [0.30,-0.37,-0.645,0,0.38,1.57]
fix_position[6][1] = [0.3,-0.27,-0.14,0,0.38,1.57]
fix_position[7][0] = [0.40,-0.33,-0.645,0,0.38,1.57]
fix_position[7][1] = [0.4,-0.27,-0.24,0,0.38,1.57]
class MoveItGripperDemo:
    def __init__(self,position):
        # 初始化move_group的API
        global fix_position
        moveit_commander.roscpp_initialize(sys.argv)

        # 初始化ROS节点
        rospy.init_node('moveit_gripper_demo', anonymous=True)
        arm = moveit_commander.MoveGroupCommander("sagittarius_arm")
        # 初始化需要使用move group控制的夹爪的group
        gripper = moveit_commander.MoveGroupCommander("sagittarius_gripper")

        # 设置夹爪运动的允许误差值
        arm.allow_replanning(True)
        
        # 设置目标位置所使用的参考坐标系
        arm.set_pose_reference_frame('world')
                
        # 设置位置(单位：米)和姿态（单位：弧度）的允许误差
        arm.set_goal_position_tolerance(0.001)
        arm.set_goal_orientation_tolerance(0.001)
        
        # 设置允许的最大速度和加速度
        arm.set_max_acceleration_scaling_factor(0.5)
        arm.set_max_velocity_scaling_factor(0.5)
        gripper.set_goal_joint_tolerance(0.001)

        # 设置允许的最大速度和加速度
        gripper.set_max_acceleration_scaling_factor(0.5)
        gripper.set_max_velocity_scaling_factor(0.5)
        arm.set_named_target('sleep')
        arm.go()
        rospy.sleep(1)
        # 控制夹爪闭合
        gripper.set_named_target('close')
        gripper.go()
        rospy.sleep(1)
        # joint_positions = [-0.00061454830783556, -0.2034660042252271, -0.149119908946021,
        #                    0.02245819323134223, -0.4085151620609834, 0.00039724354387525]
        joint_positions_1 = fix_position[position-1][0]
        arm.set_joint_value_target(joint_positions_1)
        arm.go()
        rospy.sleep(1)
        joint_positions_2 = fix_position[position-1][1]
        arm.set_joint_value_target(joint_positions_2)
        arm.go()
        rospy.sleep(1)
        #让机械臂的末端移动到指定位置
        
        # 控制夹爪打开
        # gripper.set_named_target('open')
        # gripper.go()
        # rospy.sleep(2)

        # 控制夹爪闭合
        # gripper.set_named_target('close')
        # gripper.go()
        # rospy.sleep(2)

        # # 设置夹爪的目标位置，使用两个关节的位置数据进行描述（单位：弧度）
        # joint_positions = [-0.022, -0.022]
        # gripper.set_joint_value_target(joint_positions)

        # # 控制夹爪完成运动
        # gripper.go()
        # rospy.sleep(2)

        # # 控制夹爪先回到初始化位置
        # gripper.set_named_target('open')
        # gripper.go()
        rospy.sleep(1)
        arm.set_named_target('sleep')
        arm.go()
        rospy.sleep(5)
        # 关闭并退出moveit
        # moveit_commander.roscpp_shutdown()
        # moveit_commander.os._exit(0)

def callback(data):
    global latest_image
    try:
        bridge = CvBridge()
        # 将ROS图像消息转换为OpenCV图像
        latest_image = bridge.imgmsg_to_cv2(data, "bgr8")
        cv2.imshow("Camera Image", latest_image)
        cv2.waitKey(1)
    except CvBridgeError as e:
        print(e)
if __name__ == "__main__":
    # rospy.init_node('get_image_node', anonymous=True)
    # sub = rospy.Subscriber("/usb_cam/image_raw", Image, callback)
    # rospy.spin()  # 保持节点运行
    

    try:
        MoveItGripperDemo(1)
        MoveItGripperDemo(2)
        MoveItGripperDemo(3)
        MoveItGripperDemo(4)
        MoveItGripperDemo(5)
        MoveItGripperDemo(6)
        MoveItGripperDemo(7)
        MoveItGripperDemo(8)
    except rospy.ROSInterruptException:
        pass
    moveit_commander.roscpp_shutdown()
    moveit_commander.os._exit(0)