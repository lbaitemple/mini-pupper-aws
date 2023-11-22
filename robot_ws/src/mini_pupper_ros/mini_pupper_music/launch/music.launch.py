from launch import LaunchDescription
from launch_ros.actions import Node
import os
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument, LogInfo

def generate_launch_description():

    music_config_path = os.path.join(
        get_package_share_directory('mini_pupper_music'),
        'playlists'
    )
    music_server_node = Node(
            package="mini_pupper_music",
            namespace="",
            executable="service",
            name="music_server",
            parameters=[
                {"music_config_path": music_config_path}
           ]
        )
    return LaunchDescription([
        music_server_node
    ])