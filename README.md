## Project Title
A Mahjong-playing System for RB3 Gen2 Utilizing Depth Images


## Overview
This project develops a robot arm system for RB3 Gen2 using depth images. RB3 Gen2 serves as the core hardware platform, offering advanced motion control and sensor capabilities. Depth images enable the robot arm to perceive 3D environments for tasks like object recognition and grasping. The Qualcomm Intelligent Robotics Product SDK is utilized for efficient image processing and seamless integration with RB3 Gen2, enhancing the system's performance and reliability.
## Quick Start with QualComm RB3 gen2
Download the precompiled package for RB3 Gen2：

wget https://artifacts.codelinaro.org/artifactory/qli-ci/flashable-binaries/qirpsdk/qcs6490-rb3gen2-vision-kit/arm-qcom-6.6.65-QLI.1.4-Ver.1.1_robotics-product-sdk-1.1.zip

Use the following command to unzip the package:

unzip arm-qcom-6.6.65-QLI.1.4-Ver.1.1_robotics-product-sdk-1.1.zip

The specific content is as follows:[QualComm Intelligent Robotics Product SDK Quick Start]([QIRP User Guide - Qualcomm® Linux Documentation](https://docs.qualcomm.com/bundle/publicresource/topics/80-70018-265/quick-start_3.html?vproduct=1601111740013072&version=1.4&facet=Qualcomm Intelligent Robotics Product (QIRP) SDK)


## 🦾 Project Overview

The project is based on the Sagittarius robotic arm, which includes the following components:

- **End Effector**: A gripper mounted on the arm to manipulate Mahjong tiles.
- **Drive System**: Six servo motors, each controlling one degree of freedom (DoF).
- **Sensing System**: A camera-based vision module that captures images of Mahjong tiles.
- **Control System**: A CM9.04 controller at the base of the arm, acting as the core control unit.

> ✳️ The Sagittarius robot is a six-axis (6-DoF) robotic manipulator, allowing it to imitate human-like arm motions.

## 🚀 Getting Started

### Step 1: Launch the Simulation Environment

Open a terminal and run:

```bash
roslaunch sdk_sagittarius_arm rviz_control_sagittarius.launch
```

### Step 2: Start the Mahjong Motion Controller

Open another terminal and run:

```shell
rosrun sagittarius_courses motion_controller.py __ns:=sgr532
```

## 📚 Acknowledgements

We would like to thank the AIR5021 teaching staff for their guidance, and the Sagittarius open-source team for providing the hardware/software framework.

## 📌 Notes

- The Mahjong game rules have been simplified for demonstration purposes.
- Please make sure the ROS environment and the Sagittarius SDK are properly configured.
