#!/bin/bash
source /opt/ros/humble/setup.bash
source ./install/setup.bash
export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.10/dist-packages

printenv


exec "${@:1}"
