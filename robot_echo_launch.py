from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='demo_nodes_py',
            executable='talker',
            name='cmd_parser',
            remappings=[('chatter', '/cmd_text')]
        ),
        Node(
            package='demo_nodes_py',
            executable='listener',
            name='logger_node',
            remappings=[('chatter', '/cmd_text')]
        ),
    ])
