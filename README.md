
[![GitHub issues](https://img.shields.io/github/issues/harshvs99/robotARM)](https://github.com/harshvs99/QCDashboard/issues)
[![GitHub forks](https://img.shields.io/github/forks/harshvs99/robotARM)](https://github.com/harshvs99/QCDashboard/network)
[![GitHub stars](https://img.shields.io/github/stars/harshvs99/robotARM)](https://github.com/harshvs99/QCDashboard/stargazers)
[![GitHub license](https://img.shields.io/github/license/harshvs99/robotARM)](https://github.com/harshvs99/QCDashboard/blob/master/LICENSE)

# QCDashboard
<!-- Robotic Spatial Positioning Arm built on ARM Cortex M4 Micro-controller using Servo Motors with Manual and Automated usage

## Physical Model
- Mechanical design of the robot arm is based on a robot manipulator with similar functions to a human arm. 
- Links are connected by joints to form an open kinematic chain. One end of the chain is attached to the robot base, and another end is equipped with a tool (hand, gripper, or end-effectors) which is analogous to human hand in order to perform assembly and other tasks and to interact with the environment. 
  - Two types of joint which are prismatic and rotary joints and they connect the neighbouring link. 
  - Links of the manipulator are connected by joints allowing rotational motion and the links of the manipulator is considered to form a kinematic chain.
  - A robotic arm with only four degrees of freedom is designed because it is adequate for most of the necessary movement. 
- Design of the robot arm is faced with these restrictions:
  - The length of links is assumed to be equal to satisfy spatial coding requirements
  - Gear system that allows for high-torque performance, uses harmonic drive system to deliver the required torque
  - 3D printed components from https://hackaday.io/project/18388-mammoth-arm

## Software Model 
- Standard Motor Operation
  - Different pulse widths given to specify arm angle location
  - Uses given HAL drivers for servo motor operation
- Bluetooth Module
  - HC05 Module used along with Mobile App
  - Input taken in terms of cm length along x,y,z spatial directions
  - Special command for automatic operation

## Logical Model
- Uses spatial array to store last recorded values
- Calculates rotation based on differential of new and last recorded values
- Converts given x, y, z co-ordinate system into r, \theta and \phi forms 
 -->
