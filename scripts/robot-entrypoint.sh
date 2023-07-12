#!/bin/bash
source /opt/ros/noetic/setup.bash
source /usr/share/gazebo-11/setup.sh
source ./install/setup.sh
printenv

exec "${@:1}"
