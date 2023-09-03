# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
FROM --platform=linux/arm64 tiryoh/ros2:humble-20230820T0207 AS build-base

LABEL component="com.example.ros2.minipupper"
LABEL build_step="ROSMiniPupper_Build"

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F42ED6FBAB17C654
RUN apt-get update && apt-get install python3-pip -y
RUN apt-get update && apt-get install ros-$ROS_DISTRO-example-interfaces ros-$ROS_DISTRO-robot-localization -y
RUN python3 -m pip install awsiotsdk

# ==== Package 1: ROS2 mini pupper dance script ==== 
FROM build-base AS ros-minipupper-package
LABEL component="com.example.ros2.minipupper"
LABEL build_step="ROSMiniPupperPackage_Build"


# Create user to reduce privilege
ARG USERNAME=robomaker
RUN groupadd $USERNAME && \
    useradd -ms /bin/bash -g $USERNAME $USERNAME && \
    sh -c 'echo "$USERNAME ALL=(root) NOPASSWD:ALL" >> /etc/sudoers'
    
# Switch to newly created user    
USER $USERNAME
RUN sh -c 'cd /home/$USERNAME'
# Copy our Robot and Simulation application
RUN sh -c 'mkdir -p /home/robomaker/workspace/robot_ws/src'

RUN sudo apt-get install -y python3-pip apt-utils
RUN pip install Inject==3.5.4 setuptools==58.2.0


ADD robot_ws/  /home/robomaker/workspace/robot_ws/
ADD robot_ws/src /home/robomaker/workspace/robot_ws/src

RUN sudo rosdep fix-permissions && rosdep update --include-eol-distros

WORKDIR /home/robomaker/workspace/robot_ws

RUN /bin/bash -c "source /opt/ros/humble/setup.bash && rosdep install --from-paths src --ignore-src --rosdistro=${ROS_DISTRO} --skip-keys=joint_state_publisher_gui --skip-keys=nav2_bringup --skip-keys=gazebo_plugins  --skip-keys=velodyne_gazebo_plugins --skip-keys=robot_localization -y  && colcon build      --install-base /opt/ros-minipupper-package  "
# Add entrypoint script and grant permission
COPY scripts/robot-entrypoint.sh robot-entrypoint.sh
RUN sh -c 'sudo chmod +x robot-entrypoint.sh && sudo chown robomaker:robomaker robot-entrypoint.sh'

COPY scripts/dance.sh dance.sh
RUN sh -c 'sudo chmod +x dance.sh && sudo chown robomaker:robomaker dance.sh'

# ==== Package 2: Greengrass Bridge Node ==== 
FROM build-base AS greengrass-bridge-package
LABEL component="com.example.ros2.minipupper"
LABEL build_step="GreengrassBridgeROSPackage_Build"
ARG LOCAL_WS_DIR

COPY ${LOCAL_WS_DIR}/src /ws/src
WORKDIR /ws

# Cache the colcon build directory.
RUN --mount=type=cache,target=${LOCAL_WS_DIR}/build:/ws/build \
    . /opt/ros/$ROS_DISTRO/setup.sh && \
    colcon build \
     --install-base /opt/greengrass_bridge


# ==== ROS Runtime Image (with the two packages) ====
FROM build-base AS runtime-image
LABEL component="com.example.ros2.minipupper"

COPY --from=ros-minipupper-package /opt/ros-minipupper-package /ros-minipupper-package
COPY --from=greengrass-bridge-package /opt/greengrass_bridge /opt/greengrass_bridge

CMD ros2 launch mini_pupper_bringup bringup.launch.py 
ENTRYPOINT [ "/home/robomaker/workspace/robot_ws/robot-entrypoint.sh" ]

