from launch import LaunchDescription
import os
from launch.actions import SetEnvironmentVariable
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():


    ld = LaunchDescription()
    
    dance_config_path = os.path.join(
        get_package_share_directory('mini_pupper_dance'),
        'routines'
    )

    env = SetEnvironmentVariable(
            'PYTHONPATH',
            os.pathsep.join([dance_config_path, os.environ.get('PYTHONPATH', '')])
    )
    
    dance_server_node = Node(
            package="mini_pupper_dance",
            namespace="",
            executable="service",
            name="dance_server",
        )
    dance_client_node = Node(
            package="mini_pupper_dance",
            namespace="",
            executable="client",
            name="dance_client",
        )
    pose_controller_node = Node(
            package="mini_pupper_dance",
            namespace="",
            executable="pose_controller",
            name="pose_controller",
        )
    
    dance_node = Node(
            package="mini_pupper_dance",
            namespace="",
            executable="dance",
            name="dance",
            parameters=[
                {"dance_config_path": dance_config_path}
            ]
        )    
    
    ld.add_action(env)
    ld.add_action(dance_node)    
    ld.add_action(pose_controller_node)   
    
    return ld