#!/bin/bash
source /opt/ros/humble/setup.bash
#ros2 run teleop_twist_keyboard teleop_twist_keyboard
if [ $# -lt 1 ]; then
  ros2 topic pub -1 /dance_config std_msgs/msg/String data:\ \'demo\'\ 
else 
  ros2 topic pub -1 /dance_config std_msgs/msg/String data:\ \'$1\'\ 
fi
