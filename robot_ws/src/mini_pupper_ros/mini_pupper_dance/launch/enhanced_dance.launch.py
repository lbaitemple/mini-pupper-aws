from launch import LaunchDescription
import os
from launch.actions import SetEnvironmentVariable
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument, LogInfo

def generate_launch_description():


    ld = LaunchDescription()
    
    dance_config_path = os.path.join(
        get_package_share_directory('mini_pupper_dance'),
        'routines'
    )

    joint_music_connected = LaunchConfiguration("joint_music_connected")

    declare_music_connected = DeclareLaunchArgument(
            name='joint_music_connected',
            default_value='true',
            description='Set to true if connected to a physical robot'
        )
        
    bringup_path = os.path.join(
        get_package_share_directory('mini_pupper_bringup'),
        'launch/bringup.launch.py'
    )
    
    music_path = os.path.join(
        get_package_share_directory('mini_pupper_music'),
        'launch/music.launch.py'
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
            executable="enhanced_dance",
            name="dance",
            parameters=[
                {"dance_config_path": dance_config_path,
                "joint_music_connected": joint_music_connected, 
                }
            ]
        )    

        
    launch_bringup=IncludeLaunchDescription(
            PythonLaunchDescriptionSource(bringup_path)
        )
    
    launch_music=IncludeLaunchDescription(
            PythonLaunchDescriptionSource(music_path)
        )

    ld.add_action(env)
    ld.add_action(launch_bringup)
    ld.add_action(launch_music)
    ld.add_action(dance_node)    
    ld.add_action(pose_controller_node)   
    
    return ld