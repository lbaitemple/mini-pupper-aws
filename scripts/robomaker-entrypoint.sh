#!/bin/bash

source /opt/ros/humble/setup.bash
source /opt/ros_demos/setup.bash
#source /opt/greengress_bridge/setup.bash
source /home/robomaker/workspace/robot_ws/install/setup.sh
source /opt/greengrass_bridge/setup.bash
source /opt/ros/humble/setup.bash

export PYTHONPATH=$PYTHONPATH:$DANCE_CONFIG:/usr/local/lib/python3.10/dist-packages

printenv


#exec "${@:1}"
# Execute the provided command
exec "$@"
