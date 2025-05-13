#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy, sys
import moveit_commander
import math
from moveit_commander import MoveGroupCommander
from geometry_msgs.msg import Pose
from copy import deepcopy

# Updated function to generate a five-pointed star
def generate_star_waypoints(center_pose, radius=0.1, num_points=5):
    waypoints = []
    angle_offset = math.pi / 2  # To rotate the star so it's upright

    for i in range(num_points):
        angle = 2 * math.pi * i / num_points + angle_offset
        # Calculate the outer points of the star
        pose = deepcopy(center_pose)
        pose.position.x += radius * math.cos(angle)
        pose.position.y += radius * math.sin(angle)
        waypoints.append(pose)

        # Generate inner points for the star
        angle += math.pi / num_points  # 144 degree angle for the next inner point
        pose = deepcopy(center_pose)
        pose.position.x += (radius / 2) * math.cos(angle)
        pose.position.y += (radius / 2) * math.sin(angle)
        waypoints.append(pose)

    return waypoints

class MoveItCartesianDemo:
    def __init__(self):
        # Initialize the move_group API
        moveit_commander.roscpp_initialize(sys.argv)

        # Initialize ROS node
        rospy.init_node('moveit_cartesian_demo', anonymous=True)
                        
        # Initialize the arm group for controlling the robotic arm
        arm = MoveGroupCommander('sagittarius_arm')
        
        # Allow replanning in case of failure
        arm.allow_replanning(True)
        
        # Set the reference frame for the target position
        arm.set_pose_reference_frame('world')
                
        # Set tolerances for position (meters) and orientation (radians)
        arm.set_goal_position_tolerance(0.001)
        arm.set_goal_orientation_tolerance(0.001)
        
        # Set maximum velocity and acceleration scaling factors
        arm.set_max_acceleration_scaling_factor(0.5)
        arm.set_max_velocity_scaling_factor(0.5)
        
        # Get the end effector link name
        end_effector_link = arm.get_end_effector_link()
        
        # Move the arm to the home position
        arm.set_named_target('home')
        arm.go()
        rospy.sleep(1)
                                               
        # Get the current pose to use as the starting position
        start_pose = arm.get_current_pose(end_effector_link).pose

        print(start_pose)
        
        # 初始化路点列表
        waypoints = []
                
        # 将初始位姿加入路点列表
        waypoints.append(start_pose)
            
        # 设置路点数据，并加入路点列表
        wpose = deepcopy(start_pose)
        wpose.position.z -= 0.15

        # Get the current position as the center of the star
        center_pose = arm.get_current_pose(end_effector_link).pose
        waypoints = generate_star_waypoints(center_pose)

        # Add the starting position back to the waypoints for closing the star
        waypoints.append(deepcopy(start_pose))

        fraction = 0.0   # Path planning coverage
        maxtries = 50    # Maximum attempts
        attempts = 0     # Attempt counter
        
        # Set the current state as the starting state for motion planning
        arm.set_start_state_to_current_state()
 
        # Try to plan a Cartesian path through all the waypoints
        while fraction < 1.0 and attempts < maxtries:
            (plan, fraction) = arm.compute_cartesian_path (
                                  waypoints,   # Waypoint poses
                                  0.01,        # EEF step size
                                  0.0,         # Jump threshold
                                  True)        # Avoid collisions
            
            attempts += 1
            if attempts % 10 == 0:
                rospy.loginfo("Still trying after " + str(attempts) + " attempts...")

        # Execute the plan if successful
        if fraction == 1.0:
            rospy.loginfo("Path computed successfully. Moving the arm.")
            arm.execute(plan)
            rospy.loginfo("Path execution complete.")
        else:
            rospy.loginfo("Path planning failed with only " + str(fraction) + " success after " + str(maxtries) + " attempts.")

        rospy.sleep(1)
        moveit_commander.roscpp_shutdown()
        moveit_commander.os._exit(0)

def generate_star_waypoints(center_pose, radius=0.1):
    waypoints = []  # 用来存储五角星路径的所有路点
    angle_offset = math.radians(-90)  # 起始角度调整为-90度，这样五角星的尖端朝上
    points = []  # 存储五角星的五个顶点
    
    # 计算五个顶点
    for i in range(5):
        angle = angle_offset + i * 2 * math.pi / 5  # 每个顶点的角度，5个顶点均匀分布在圆上
        x = center_pose.position.x + radius * math.cos(angle)  # x坐标 = 半径 * cos(角度)
        y = center_pose.position.y + radius * math.sin(angle)  # y坐标 = 半径 * sin(角度)
        p = deepcopy(center_pose)  # 创建一个起始位置的副本
        p.position.x = x  # 设置该点的x坐标
        p.position.y = y  # 设置该点的y坐标
        points.append(p)  # 将这个顶点添加到顶点列表中
    
    # 五角星的连接顺序是：0 → 2 → 4 → 1 → 3 → 0
    order = [0, 2, 4, 1, 3, 0]  # 连接点的顺序，注意最后一个点是0点，形成闭环
    
    # 按照顺序将顶点连接为路径
    for i in order:
        waypoints.append(deepcopy(points[i]))  # 将连接的点添加到路径中

    return waypoints  # 返回生成的路径

def interpolate_points(p1, p2, num_points=10):
    # 使用线性插值在两个点之间生成更多的路径点
    points = []
    for i in range(num_points):
        alpha = i / float(num_points)
        interpolated_point = deepcopy(p1)
        interpolated_point.position.x = p1.position.x + alpha * (p2.position.x - p1.position.x)
        interpolated_point.position.y = p1.position.y + alpha * (p2.position.y - p1.position.y)
        points.append(interpolated_point)
    return points

def plan_and_execute(arm, waypoints):
    fraction = 0.0
    maxtries = 100  # 增加最大尝试次数
    attempts = 0

    arm.set_start_state_to_current_state()
    while fraction < 1.0 and attempts < maxtries:
        (plan, fraction) = arm.compute_cartesian_path(
            waypoints,     # 路点列表
            0.005,         # 更小的步进值，之前是 0.01
            0.0,           # jump_threshold
            True           # avoid_collisions
        )
        attempts += 1
        if attempts % 10 == 0:
            rospy.loginfo("Still trying after " + str(attempts) + " attempts...")

    if fraction == 1.0:
        rospy.loginfo("Path computed successfully. Moving the arm.")
        arm.execute(plan)
        rospy.loginfo("Path execution complete.")
    else:
        rospy.loginfo("Path planning failed with only " + str(fraction) + " success after " + str(maxtries) + " attempts.")



class MoveItCartesianDemo:
    def __init__(self):
        # 初始化move_group的API
        moveit_commander.roscpp_initialize(sys.argv)

        # 初始化ROS节点
        rospy.init_node('moveit_cartesian_demo', anonymous=True)
                        
        # 初始化需要使用move group控制的机械臂中的arm group
        arm = MoveGroupCommander('sagittarius_arm')
        
        # 当运动规划失败后，允许重新规划
        arm.allow_replanning(True)
        
        # 设置目标位置所使用的参考坐标系
        arm.set_pose_reference_frame('world')
                
        # 设置位置(单位：米)和姿态（单位：弧度）的允许误差
        arm.set_goal_position_tolerance(0.001)
        arm.set_goal_orientation_tolerance(0.001)
        
        # 设置允许的最大速度和加速度
        arm.set_max_acceleration_scaling_factor(0.5)
        arm.set_max_velocity_scaling_factor(0.5)
        
        # 获取终端link的名称
        end_effector_link = arm.get_end_effector_link()
        # 控制机械臂先回到初始化位置
        arm.set_named_target('home')
        arm.go()
        rospy.sleep(1)
                                               
        # 获取当前位姿数据最为机械臂运动的起始位姿
        start_pose = arm.get_current_pose(end_effector_link).pose

        print (start_pose)
        
        # 使用上面的代码生成五角星路径，并插值增加更多的路径点
        center_pose = arm.get_current_pose(end_effector_link).pose
        waypoints = generate_star_waypoints(center_pose)

        # 使用插值方法平滑路径
        interpolated_waypoints = []
        for i in range(len(waypoints) - 1):
            interpolated_waypoints.extend(interpolate_points(waypoints[i], waypoints[i+1]))

        # 最后一个点与第一个点也需要连接
        interpolated_waypoints.extend(interpolate_points(waypoints[-1], waypoints[0]))

        # 执行路径规划
        plan_and_execute(arm, interpolated_waypoints)

        fraction = 0.0   #路径规划覆盖率
        maxtries = 50   #最大尝试规划次数
        attempts = 0     #已经尝试规划次数
        
        # 设置机器臂当前的状态作为运动初始状态
        arm.set_start_state_to_current_state()
 
        # 尝试规划一条笛卡尔空间下的路径，依次通过所有路点
        while fraction < 1.0 and attempts < maxtries:
            (plan, fraction) = arm.compute_cartesian_path (
                                  waypoints,   # waypoint poses，路点列表
                                  0.01,        # eef_step，终端步进值
                                  0.0,         # jump_threshold，跳跃阈值
                                 True)        # avoid_collisions，避障规划
            
            # 尝试次数累加
            attempts += 1
            # 打印运动规划进程
            if attempts % 10 == 0:
                rospy.loginfo("Still trying after " + str(attempts) + " attempts...")
        # 如果路径规划成功（覆盖率100%）,则开始控制机械臂运动
        if fraction == 1.0:
            rospy.loginfo("Path computed successfully. Moving the arm.")
            arm.execute(plan)
            rospy.loginfo("Path execution complete.")
        # 如果路径规划失败，则打印失败信息
        else:
            rospy.loginfo("Path planning failed with only " + str(fraction) + " success after " + str(maxtries) + " attempts.")  

        rospy.sleep(1)
        # 如果路径规划成功（覆盖率100%）,则开始控制机械臂运动
        if fraction == 1.0:
            rospy.loginfo("Path computed successfully. Moving the arm.")
            arm.execute(plan)
            rospy.loginfo("Path execution complete.")
        # 如果路径规划失败，则打印失败信息
        else:
            rospy.loginfo("Path planning failed with only " + str(fraction) + " success after " + str(maxtries) + " attempts.")  

        rospy.sleep(1)
        moveit_commander.roscpp_shutdown()
        moveit_commander.os._exit(0)

if __name__ == "__main__":
    try:
        MoveItCartesianDemo()
    except rospy.ROSInterruptException:
        pass