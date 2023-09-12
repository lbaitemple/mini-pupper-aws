# Set main arguments.
ARG ROS_DISTRO=humble
ARG LOCAL_WS_DIR=workspace

# ==== ROS Build Stages ====

# ==== Base ROS Build Image ====
FROM --platform=linux/arm64 ros:${ROS_DISTRO}-ros-base AS build-base
LABEL component="com.example.ros2.demo"
LABEL build_step="ROSDemoNodes_Build"

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F42ED6FBAB17C654
RUN apt-get update && apt-get install python3-pip -y
RUN apt-get update && apt-get install ros-$ROS_DISTRO-xacro
RUN python3 -m pip install  Inject==3.5.4 setuptools==58.2.0 awsiotsdk

# ==== Package 1: ROS Demos Talker/Listener ==== 
FROM build-base AS ros-mini_pupper-package
LABEL component="com.example.ros2.mini_pupper_v2"
LABEL build_step="DemoNodesROSPackage_Build"

# Clone the demos_ros_cpp package from within the ROS Demos monorepo.
RUN mkdir -p /ws/src
WORKDIR /tmp

# install mangdang v2
RUN bash -c 'git clone https://github.com/mangdangroboticsclub/mini_pupper_2_bsp'
WORKDIR /tmp/mini_pupper_2_bsp/Python_Module
RUN python3 setup.py install

ADD robot_ws/src /ws/src
WORKDIR /ws
RUN . /opt/ros/$ROS_DISTRO/setup.sh && \
    rosdep install --from-paths src --ignore-src --rosdistro=${ROS_DISTRO} \
    --skip-keys=joint_state_publisher_gui --skip-keys=rviz2 \
    --skip-keys=nav2_bringup --skip-keys=gazebo_plugins \
    --skip-keys=velodyne_gazebo_plugins -y && \
    colcon build --build-base workspace/build --install-base /opt/ros_demos

# ==== ROS Runtime Image (with the two packages) ====
FROM build-base AS runtime-image
LABEL component="com.example.ros2.mini_pupper_v2"

COPY --from=ros-mini_pupper-package /opt/ros_demos /opt/ros_demos

WORKDIR /
COPY scripts/robot-entrypoint.sh  /robot-entrypoint.sh
RUN chmod +x /robot-entrypoint.sh
ENTRYPOINT ["/robot-entrypoint.sh"]

