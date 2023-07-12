#!/bin/bash
source /opt/ros/noetic/setup.bash
source /usr/share/gazebo-9/setup.sh
source ./install/setup.sh
printenv

exec "${@:1}"
