#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy, sys
import moveit_commander
from geometry_msgs.msg import PoseStamped, Pose

class MoveItIkDemo:
    def __init__(self):
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('moveit_ik_demo')

        arm = moveit_commander.MoveGroupCommander("sagittarius_arm")
        end_effector_link = arm.get_end_effector_link()
        reference_frame = 'world'
        arm.set_pose_reference_frame(reference_frame)

        arm.allow_replanning(True)
        arm.set_goal_position_tolerance(0.001)
        arm.set_goal_orientation_tolerance(0.001)
        arm.set_max_acceleration_scaling_factor(0.5)
        arm.set_max_velocity_scaling_factor(0.5)

        arm.set_named_target('Home')
        arm.go()
        rospy.sleep(1)

        target_pose = PoseStamped()
        target_pose.header.frame_id = reference_frame
        target_pose.header.stamp = rospy.Time.now()
        target_pose.pose.position.x = 0.2472990396168796
        target_pose.pose.position.y = 0.0006590926103004068
        target_pose.pose.position.z = 0.3456034504080325
        target_pose.pose.orientation.w = 1.0

        arm.set_start_state_to_current_state()
        arm.set_pose_target(target_pose, end_effector_link)

        plan_success, traj, planning_time, error_code = arm.plan()

        arm.execute(traj)
        rospy.sleep(1)

        arm.set_named_target('Sleep')
        arm.go()

        moveit_commander.roscpp_shutdown()
        moveit_commander.os._exit(0)

if __name__ == "__main__":
    MoveItIkDemo()
