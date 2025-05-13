# CUHKSZ-AIR5021-Team12-Final

本项目为香港中文大学（深圳）MAIR-AIR5021 课程的 Final Project，由 Team 12 完成。

我们基于 Sagittarius 六轴机械臂，设计了一个可以简化麻将游戏的系统，能够完成 **麻将识别、决策与执行动作**。

## 🦾 项目简介

本项目使用的是 Sagittarius 六轴机械臂。其主要结构包括：

- **执行机构**：末端夹爪，可夹取麻将牌。
- **驱动系统**：6 个伺服电机，分别控制每个自由度。
- **传感系统**：包括摄像头，用于获取麻将牌图像。
- **控制系统**：CM9.04 控制器，作为机械臂的大脑执行任务指令。

> ✳️ 六轴机械臂即拥有 6 个自由度，可模拟人类手臂的复杂运动。

## 🚀 快速启动

### Step 1：启动仿真环境

打开一个终端运行：

```bash
roslaunch sdk_sagittarius_arm rviz_control_sagittarius.launch
```

### Step 2：启动麻将动作控制程序

打开另一个终端运行：

```shell
rosrun sagittarius_courses motion_controller.py __ns:=sgr532
```

## 📚 致谢

感谢 CUHKSZ MAIR AIR5021 教学团队提供支持与平台，也感谢 Sagittarius 开源项目对我们开发的帮助。

## 📌 注意事项

- 本项目简化了麻将规则，仅用于演示识别与机械动作。
- 请确保你已经正确配置好 ROS 环境与 SDK。
