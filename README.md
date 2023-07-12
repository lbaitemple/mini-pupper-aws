# MiniPupper AWS

The README is out of date.

## general docker commands
```
docker rmi -f $(docker images -aq)
```

## Activity 1: Simulate the Dance Robot

### Step 1: Setup the RoboMaker IDE

choose 
**Cloud 9**, 

 1: **Create Environment** 

 2. **New EC2 instance, Additional instance types, c4.xlarge, Ubuntu Server 18.04, Secure Shell (SSH)**

 3. **setup ROS Melodic** by running ```curl -fsSL "http://bit.ly/robomaker" | sudo -E bash -```

 4. **wait for 10 minues installation, then restart the instance by typing**
```sudo reboot```

### Step 2: Setup docker for Robot and Simulation Applications
* Clone Packages

```sh
git clone https://github.com/lbaitemple/mini-pupper-aws

```

Copy the following docker command for each line
```
cd mini-pupper-aws
docker build . -t mini-pupper-base:1.0 -f Dockerfile-Base
docker build . -t mini-pupper-robot:1.0 -f Dockerfile-Robot
docker build . -t mini-pupper-simulation:1.0 -f Dockerfile-Simulation
```

You can run
```
docker image list
```


to see if three docker instances avaiable. Then, in terminal 1 you can
```
docker run -it --net=host --privileged \
-e DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix/ \
-u robomaker -e GAZEBO_MASTER_URI=http://localhost:5555 \
-e ROS_MASTER_URI=http://localhost:11311 \
mini-pupper-robot:1.0
```
Make sure you start gazebo screen, by ***preview, preview running application***. In the new terminal, click on **popuup** next to the **broswer**.

For the first setup, you need to make sure you click on the screen and allow the connection

Go back to the cloud 9, start the second terminal windoe
```
docker run -it --net=host --privileged \
-e DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix/ \
-u robomaker -e GAZEBO_MASTER_URI=http://localhost:5555 \
-e ROS_MASTER_URI=http://localhost:11311 \
mini-pupper-simulation:1.0
```

You should be able to the mini pupeert in the gazebo window
###  Step 2: Upload the containers to Amazon ECR

1. Navigate to the Amazon ECR console
2. In the navigation pane, choose Create Repository
3. For Repository Name, specify the name of repository. For this workshop, enter mini-pupper-robot
4. Choose Create Repository

#### Tag your images (the best way is to look at the pull command section)
```
docker tag mini-pupper-robot:1.0 111122223333.dkr.ecr.your-region.amazonaws.com/mini-pupper-robot:1.0
docker push 111122223333.dkr.ecr.your-region.amazonaws.com/mini-pupper-robot:1.0


docker tag mini-pupper-simulation:1.0 111122223333.dkr.ecr.your-region.amazonaws.com/mini-pupper-simulation:1.0
docker push 111122223333.dkr.ecr.your-region.amazonaws.com/mini-pupper-simulation:1.0
```
where you will need to replace 111122223333 with your 12-digit AWS account number, and your-region with your region. 

With the registry uploaded with docker images, we can run the robot application and the simulation applicaiton in AWS Robomaker

Just select ECR repository to load image to each application accordingly

After that, we can create a simulation job with these two applications. You will need to setup to Networking.

For Robot Application, choose the previously created robot application mini-pupper-robot
For Launch Command, specify the launch command as a comma-separated list of arguments. In this workshop, enter roslaunch, mini_pupper_dance, dance.launch, hardware_connected:=false

Choose Add item and add the following to the Environment variables

Name	Value

GAZEBO_MASTER_URI	http://ROBOMAKER_SIM_APP_IP:11345

ROS_IP	ROBOMAKER_ROBOT_APP_IP

ROS_MASTER_URI	http://ROBOMAKER_ROBOT_APP_IP:11311


In the Specify simulation application page, you set the launch configuration of the simulation application.

For Simulation Application, choose the previously created simulation application mini-pupper-simulation
For Launch Command, specify the launch command as a comma separated list of arguments. 

In this workshop, enter roslaunch, mini_pupper_simulation, aws_stage.launch

Select Run with streaming session to enable streaming the Gazebo GUI
For Environment variables specify the following environment variables.

Name	Value
GAZEBO_MASTER_URI	http://ROBOMAKER_SIM_APP_IP:11345

ROS_IP	ROBOMAKER_SIM_APP_IP

ROS_MASTER_URI	http://ROBOMAKER_ROBOT_APP_IP:11311

Select Simulation Application Tools then Customize tools, then Add tool

In the Add tool window, set Name to xterm, and Command to /usr/bin/xterm

For Exit behavior choose Restart from the drop-down

Make sure the radio button next to Enable UI streaming is checked

Check the box next to Send output to Amazon CloudWatch

Click on Add tool to add the xterm tool

### Step 2: Build the Robot and Simulation Applications in AWS Cloud9 

* Clone Packages

```sh
cd ~/environment/mini-pupper-aws
pip install Inject==3.5.4
sudo rosdep fix-permissions && rosdep update --include-eol-distros
cd robot_ws
rosdep install --from-paths src --ignore-src --rosdistro=${ROS_DISTRO} -y
colcon build
cd ../simulation_ws
colcon build
```

* Install Dependencies

```sh
sudo apt-get update
sudo apt install -y ros-melodic-ecl-threads ros-melodic-pointcloud-to-laserscan ros-melodic-amcl ros-melodic-velodyne-gazebo-plugins ros-melodic-ros-controllers ros-melodic-joint-state-publisher-gui ros-melodic-joint-state-publisher-gui ros-melodic-hector-sensors-description ros-melodic-base-local-planner ros-melodic-rosserial
sudo apt install -y ros-melodic-hector-gazebo-plugins   ros-melodic-dwa-local-planner ros-melodic-robot-localization ros-melodic-navfn ros-melodic-global-planner ros-melodic-move-base ros-melodic-map-server  ros-melodic-octomap-server   ros-melodic-hector-mapping ros-melodic-gmapping           
cd mini-pupper-aws/robot_ws
rosdep install --from src -i -y
```

* Compile Robot Applications and Set Executable

```sh
colcon build
cd install/mini_pupper_dance/share/mini_pupper_dance/scripts/
sudo chmod +x *
```

* Compile Simulation Package

```sh
cd ~/environment/mini-pupper-aws/simulation_ws/
colcon build
```

### Step 3: Run the Simulation

* Launch Simulation

```sh
# terminal 1
export DISPLAY=:1
source /opt/ros/melodic/setup.bash
source ~/environment/mini-pupper-aws/simulation_ws/install/setup.bash
source ~/environment/mini-pupper-aws/robot_ws/install/setup.bash
# Add meshes to Gazbo paths
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$(rospack find mini_pupper_simulation)/worlds/meshes
roslaunch mini_pupper_simulation aws_stage.launch
```

* Launch Robot Application (Dancing Demo)

```sh
# terminal 2
source /opt/ros/melodic/setup.bash
source ~/environment/mini-pupper-aws/simulation_ws/install/setup.bash
source ~/environment/mini-pupper-aws/robot_ws/install/setup.bash
roslaunch mini_pupper_dance dance.launch hardware_connected:=false
```

* Send a Message to Make Robot Dancing

```sh
# terminal 3
source /opt/ros/melodic/setup.bash
rostopic pub /dance_config std_msgs/String "data: 'demo'"
```

### Step 4: Modify the Dance Routine

* Create a new Python file in the robot application folder. Example: my_demo.py

```sh
cd ~/mini-pupper-aws/routines
touch my_demo.py
```

* Copy this template into the new file.

```python
#!/usr/bin/env python

# the duration of every command
interval_time = 0.6 # seconds

# there are 10 commands you can choose:
# move_forward: the robot will move forward
# move_backward: the robot will move backward
# move_left: the robot will move to the left
# move_right: the robot will move to the right
# look_up: the robot will look up
# look_down: the robot will look down
# look_left: the robot will look left
# look_right: the robot will look right
# stop: the robot will stop the last command and return to the default standing posture
# stay: the robot will keep the last command
dance_commands = [
'move_forward',
'stop',
'look_down',
'look_up',

'move_backward',
'stop',
'look_left',
'look_right',

'move_left',
'stop',
'look_up',
'look_left',

'move_right',
'stop',
'look_down',
'look_right',

'look_up',
'look_left',
'look_down',
'look_right',

'look_down',
'look_left',
'look_up',
'look_right'
]
```

* Modify the file, changing the name, artist, and the dance steps.
* Save your new dance routine. If not already open, open two command line tabs in the RoboMaker IDE.
* Build and Source and run the ROS application.

```sh
# terminal 1, launch simulation
export DISPLAY=:1
source /opt/ros/melodic/setup.bash
source ~/mini-pupper-aws/simulation_ws/install/setup.bash
source ~/mini-pupper-aws/robot_ws/install/setup.bash
roslaunch mini_pupper_simulation aws_stage.launch
```

```sh
# terminal 2, launch robot application
source /opt/ros/melodic/setup.bash
source ~/mini-pupper-aws/simulation_ws/install/setup.bash
source ~/mini-pupper-aws/robot_ws/install/setup.bash
roslaunch mini_pupper_dance dance.launch hardware_connected:=false
```

* Send a Message to Make Robot Dance

```sh
# terminal 3, send a message to specify which dance routine you choose
source /opt/ros/melodic/setup.bash
rostopic pub /dance_config std_msgs/String "data: 'my_demo'"
```

## Activity 2: Deploy and Run the Dance Robot

We haven't done this greengrass part yet. If you want to test the dancing routines on real robot, please refer to the follow instructions. The repository cloned on real robot is the same repository cloned in this repo.
Please also refer to our pre-build image file, [20220521.1707.V0.2.MiniPupper_remars_RoboMakerSimulation.ROS_Ubuntu21.10.0.img](https://drive.google.com/drive/folders/1gl-S3kokcna5GoSeIXZ5TD5rQhk48ALX?usp=sharing).

```sh
# on Mini Pupper's Terminal
# clone this repo
# if you use our pre-build image file,no need to execute the below 4 line commands
cd ~
git clone https://github.com/mrkoz/mini-pupper-aws.git
cd mini-pupper-aws/robot_ws
catkin_make
```

```sh
# terminal 1
source /opt/ros/melodic/setup.bash
source ~/mini-pupper-aws/robot_ws/devel/setup.bash
roslaunch mini_pupper_dance dance.launch dance_config_path:=/home/ubuntu/mini-pupper-aws/routines
```

```sh
# terminal 2
source /opt/ros/melodic/setup.bash
rostopic pub /dance_config std_msgs/String "data: 'demo'"
```

As for control in Docker, please refer to the below setting and the pre-build image sample [mini_pupper_remars_docker_IPDisplay.20220513](https://drive.google.com/drive/folders/1gl-S3kokcna5GoSeIXZ5TD5rQhk48ALX?usp=sharing).

```sh
sudo docker run -id --name ros_noetic --network host \
--privileged -v /dev:/dev -e DISPLAY=$DISPLAY -e QT_X11_NO_MITSHM=1 \
-v /sys/class/pwm:/sys/class/pwm \
-v /sys/bus/i2c/devices/3-0050/eeprom:/sys/bus/i2c/devices/3-0050/eeprom \
-v /sys/class/pwm:/sys/class/pwm \
-v /sys/bus/i2c/devices/3-0050/eeprom:/sys/bus/i2c/devices/3-0050/eeprom \
0nhc/mnpp:test
sudo xhost +
```
# Attribution

["Simple Concert Stage"](https://sketchfab.com/3d-models/simple-concert-stage-d5c7733d06d24947bf60b3a0fe203f69) by [mertbbicak](https://sketchfab.com/mertbbicak) is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). AWS banner has been added to the model.
