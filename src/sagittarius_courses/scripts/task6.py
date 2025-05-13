#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy, sys
import moveit_commander

class MoveItGripperDemo:
    def __init__(self):
        # 初始化move_group的API
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
        joint_positions = [-0.00061454830783556, -0.2034660042252271, -0.149119908946021,
                           0.02245819323134223, -0.4085151620609834, 0.00039724354387525]
        arm.set_joint_value_target(joint_positions)
        arm.go()
        rospy.sleep(1)
        #让机械臂的末端移动到指定位置
        
        # 控制夹爪打开
        gripper.set_named_target('open')
        gripper.go()
        rospy.sleep(2)

        # 控制夹爪闭合
        gripper.set_named_target('close')
        gripper.go()
        rospy.sleep(2)

        # 设置夹爪的目标位置，使用两个关节的位置数据进行描述（单位：弧度）
        joint_positions = [-0.022, -0.022]
        gripper.set_joint_value_target(joint_positions)

        # 控制夹爪完成运动
        gripper.go()
        rospy.sleep(2)

        # 控制夹爪先回到初始化位置
        gripper.set_named_target('open')
        gripper.go()
        rospy.sleep(1)

        # 关闭并退出moveit
        moveit_commander.roscpp_shutdown()
        moveit_commander.os._exit(0)

if __name__ == "__main__":
    try:
        MoveItGripperDemo()
    except rospy.ROSInterruptException:
        pass