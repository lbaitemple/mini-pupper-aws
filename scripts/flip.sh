source /opt/ros/humble/setup.bash

ros2 service call /gazebo/set_model_state '{model_state: { model_name: "mini_pupper", pose: { position: {x: 0, y: 2.7, z: 0.55}, orientation: {x: 0, y: 0, z: -1.55, w: 1} }, twist: { linear: {x: 0 , y: 0 ,z: 0} , angular: {x: 0 , y: 0 , z: 0} } , reference_frame: world } }'
