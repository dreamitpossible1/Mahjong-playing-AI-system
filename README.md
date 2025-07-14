## Project Title
Vision-Language Model-Based Mahjong AI System for RB3 Gen2


## Overview
This project develops a Mahjong-playing AI system for the RB3 Gen2 platform based on Vision-Language Models (VLMs). As the core hardware platform, RB3 Gen2 enables the system to process both visual and natural language information simultaneously through the integration of VLMs, allowing for accurate recognition and understanding of Mahjong tiles and game states.Unlike traditional approaches that rely solely on depth images, this system adopts multimodal inputs—such as RGB images and linguistic context—and processes them through VLMs to achieve a more comprehensive understanding of the game environment. The system analyzes the current game situation and formulates strategies accordingly, enabling the robot to play Mahjong intelligently and adaptively.
## Quick Start with QualComm RB3 gen2
Download the precompiled package for RB3 Gen2：

wget https://artifacts.codelinaro.org/artifactory/qli-ci/flashable-binaries/qirpsdk/qcs6490-rb3gen2-vision-kit/arm-qcom-6.6.65-QLI.1.4-Ver.1.1_robotics-product-sdk-1.1.zip

Use the following command to unzip the package:

unzip arm-qcom-6.6.65-QLI.1.4-Ver.1.1_robotics-product-sdk-1.1.zip


Before you start, make sure finish [QualComm Intelligent Robotics Product SDK Quick Start]([QIRP User Guide - Qualcomm® Linux Documentation](https://docs.qualcomm.com/bundle/publicresource/topics/80-70018-265/quick-start_3.html?vproduct=1601111740013072&version=1.4&facet=Qualcomm Intelligent Robotics Product (QIRP) SDK)


## Quick Start with uArm Swift Pro

1. Download [uArm-Python-SDK]https://github.com/uArm-Developer/uArm-Python-SDK.git

```bash
git clone https://github.com/uArm-Developer/uArm-Python-SDK.git
```
2. Installation
```bash
   python setup.py install
```


## 🦾 Project Overview

This project is based on the uArm Swift Pro robotic arm, which mainly consists of the following components:

- **End Effector**: Equipped with a suction pump, used for picking up and moving Mahjong tiles.
- **Drive System**: Composed of four servo motors, each controlling one degree of freedom (4-DoF), enabling precise and smooth motion control.
- **Control System**: An integrated controller that supports both Arduino and Python development environments, serving as the core control unit of the robotic arm.
 
> ✳️ The uArm Swift Pro is a four-axis (4-DoF) robotic manipulator known for its high precision and repeatability, making it ideal for lightweight object manipulation and interactive gaming tasks.


## 🚀 Getting Started

### Step 1: Launch the Simulation Environment

Open a terminal and run:

```bash
./run.sh
```

### Step 2: Start the Mahjong Motion Controller

Open another terminal and run:

```shell
python socket_user_majiang.py
```

📹 Results Display

[Display](https://github.com/dreamitpossible1/Mahjong-playing-AI-system/blob/main/Mahjong-playing-AI-system.mp4）


## Reference

- [Qualcomm Linux](https://www.qualcomm.com/developer/software/qualcomm-linux)

- [QualComm Intelligent Robotics Product SDK](https://docs.qualcomm.com/bundle/publicresource/topics/80-70018-265/introduction_1.html?vproduct=1601111740013072&version=1.4&facet=Qualcomm Intelligent Robotics Product (QIRP) SDK)

