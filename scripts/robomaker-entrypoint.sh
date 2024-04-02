#!/bin/bash

source /opt/ros/humble/setup.bash
#source /opt/ros_demos/setup.bash
#source /opt/greengress_bridge/setup.bash
source /home/robomaker/workspace/robot_ws/install/setup.sh
#source /opt/greengrass_bridge/setup.bash
source /opt/ros/humble/setup.bash
export DANCE_CONFIG=/home/robomaker/routines
export PYTHONPATH=$PYTHONPATH:$DANCE_CONFIG:/usr/local/lib/python3.10/dist-packages

printenv
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${IOT_ENDPOINT}
aws s3 sync  s3://${ROS_S3}/artifacts/routines /home/robomaker/routines


#exec "${@:1}"
# Execute the provided command
exec "$@"
