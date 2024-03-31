from launch import LaunchDescription
from launch_ros.actions import Node
import os
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.conditions import IfCondition


def generate_launch_description():

    joint_music_connected = LaunchConfiguration("joint_music_connected")

    declare_music_connected = DeclareLaunchArgument(
            name='joint_music_connected',
            default_value='true',
            description='Set to true if connected to a physical robot'
        )
        
    music_config_path = os.path.join(
        get_package_share_directory('mini_pupper_music'),
        'playlists'
    )
    music_server_node = Node(
            package="mini_pupper_music",
            namespace="",
            executable="service",
            name="music_server",
            condition=IfCondition(joint_music_connected),
            parameters=[
                {
                "music_config_path": music_config_path,
                "joint_music_connected": joint_music_connected,    
                }
           ]
        )
    return LaunchDescription([
        music_server_node
    ])