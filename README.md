# CUHKSZ-AIR5021-Team12-Final

This project is the final assignment for the AIR5021 course at The Chinese University of Hong Kong, Shenzhen, developed by Team 12.

We designed a simplified Mahjong-playing system using a **Sagittarius 6-DOF robotic arm**, capable of recognizing tiles, making decisions, and executing motions.

---

## 🦾 Project Overview

The project is based on the Sagittarius robotic arm, which includes the following components:

- **End Effector**: A gripper mounted on the arm to manipulate Mahjong tiles.
- **Drive System**: Six servo motors, each controlling one degree of freedom (DoF).
- **Sensing System**: A camera-based vision module that captures images of Mahjong tiles.
- **Control System**: A CM9.04 controller at the base of the arm, acting as the core control unit.

> ✳️ The Sagittarius robot is a six-axis (6-DoF) robotic manipulator, allowing it to imitate human-like arm motions.

### Mechanical Structure of Sagittarius Robot:

*(Please upload the image to the repository and reference it properly. Example below:)*

![Sagittarius Robot](images/sagittarius_arm.jpg)

---

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

------

## 📌 Notes

- The Mahjong game rules have been simplified for demonstration purposes.
- Please make sure the ROS environment and the Sagittarius SDK are properly configured.