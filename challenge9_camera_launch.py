from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'resolution',
            default_value='720p',
            description='Résolution de la caméra'
        ),
        DeclareLaunchArgument(
            'fps',
            default_value='30',
            description='Frames par seconde'
        ),
        Node(
            package='demo_nodes_cpp',
            executable='talker',
            name='camera_node',
            parameters=[{
                'resolution': LaunchConfiguration('resolution'),
                'fps': LaunchConfiguration('fps'),
            }]
        )
    ])
