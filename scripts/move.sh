#!/bin/bash
source /opt/ros/humble/setup.bash
#ros2 run teleop_twist_keyboard teleop_twist_keyboard
ros2 topic pub -1 /dance_config std_msgs/msg/String data:\ \'demo\'\ 