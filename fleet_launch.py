from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('num_robots', default_value='3'),
        DeclareLaunchArgument('monitor_freq', default_value='1.0'),

        Node(
            package='demo_nodes_py',
            executable='talker',
            name='robot_simulator_1',
        ),
        Node(
            package='demo_nodes_py',
            executable='talker',
            name='robot_simulator_2',
        ),
        Node(
            package='demo_nodes_py',
            executable='talker',
            name='robot_simulator_3',
        ),
    ])
