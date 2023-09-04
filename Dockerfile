# Source is previously built image
FROM --platform=linux/arm64  ros:humble

ENV DEBIAN_FRONTEND noninteractive
# Install common dependency and ROS tools
RUN apt-get update && apt-get install -y \
    lsb  \
    git \
    unzip \
    wget \
    curl \
    sudo \
    python3-vcstool \
    python3-pip \
    python3-rosinstall \
    python3-colcon-common-extensions

ENV QT_X11_NO_MITSHM=1

# Create user to reduce privilege
ARG USERNAME=robomaker
RUN groupadd $USERNAME && \
    useradd -ms /bin/bash -g $USERNAME $USERNAME && \
    bash -c 'echo "$USERNAME ALL=(root) NOPASSWD:ALL" >> /etc/sudoers'
    
# Switch to newly created user    
USER $USERNAME
RUN bash -c 'cd /home/$USERNAME'
RUN bash -c 'mkdir -p /home/robomaker/workspace/robot_ws/src && cd /home/robomaker/workspace'

#RUN sudo apt-get install -y python-pip apt-utils
RUN python3 -m pip install Inject==3.5.4 setuptools==58.2.0 awsiotsdk
# install mangdang v2
WORKDIR /home/robomaker/workspace
RUN bash -c 'git clone https://github.com/mangdangroboticsclub/mini_pupper_2_bsp'
WORKDIR /home/robomaker/workspace/mini_pupper_2_bsp/Python_Module
RUN sudo python3 setup.py install
#RUN pip install -e "vcs+protocol://github.com/mangdangroboticsclub/mini_pupper_2_bsp/#egg=pkg&subdirectory=Python_Module"

ADD robot_ws/src /home/robomaker/workspace/robot_ws/src
RUN sudo rosdep fix-permissions && rosdep update --include-eol-distros

WORKDIR /home/robomaker/workspace/robot_ws


# Build the Robot application
RUN bash -c 'source /opt/ros/humble/setup.bash && rosdep install --from-paths src --ignore-src --rosdistro=${ROS_DISTRO} --skip-keys=joint_state_publisher_gui --skip-keys=nav2_bringup --skip-keys=gazebo_plugins  --skip-keys=velodyne_gazebo_plugins -y  && colcon build && sudo apt clean'

# Add entrypoint script and grant permission
COPY scripts/robot-entrypoint.sh robot-entrypoint.sh
RUN bash -c 'sudo chmod +x robot-entrypoint.sh && sudo chown robomaker:robomaker robot-entrypoint.sh'

RUN sudo mkdir -p /config/certs/

# xterm for interactive debug
#RUN sudo apt install -y xterm

#CMD roslaunch mini_pupper_dance dance.launch hardware_connected:=false
ENTRYPOINT [ "/home/robomaker/workspace/robot_ws/robot-entrypoint.sh" ]