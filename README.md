## Project Title
Mahjong-playing AI System for RB3 Gen2 Using Depth Images


## Overview
This project creates a Mahjong-playing AI system for RB3 Gen2, incorporating depth images. RB3 Gen2 acts as the core hardware platform with advanced motion control and sensors. Depth images let the robot arm perceive 3D environments for recognizing and grasping Mahjong tiles. The Qualcomm Intelligent Robotics Product SDK is used for efficient image processing and integration with RB3 Gen2, boosting the system's performance and reliability. Additionally, AI algorithms are employed to analyze game situations and make strategic decisions, enabling the robot to play Mahjong effectively.
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
