# Copyright 2022 Andrew Symington
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os

from ament_index_python.packages import get_package_share_directory

import launch
from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument, ComposableNodeContainer
from launch_ros.descriptions import ComposableNode
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

BAG_FILE = os.path.join(launch.logging.launch_config.log_dir, "libsurvive.bag")
CFG_FILE = os.path.join(
    get_package_share_directory('libsurvive_ros2'), 'config', 'config.json'
)

def generate_launch_description():
    return LaunchDescription([
        
        # Options to launch
        DeclareLaunchArgument('composable', default_value='false',
            description='Launch in a composable container'),
        DeclareLaunchArgument('rosbridge', default_value='false',
            description='Launch a rosbridge'),
        DeclareLaunchArgument('record', default_value='false',
            description='Record data with rosbag'),
        
        # Non-composable launch (regular node) 
        Node(
            package='libsurvive_ros2',
            executable='libsurvive_ros2_node',
            name='libsurvive_ros2_node',
            condition=UnlessCondition(LaunchConfiguration('composable')),
            output='screen',
            arguments=[
                # '--force-calibrate', '1',
                # '--globalscenesolver', '1',
                # '--lighthouse-gen', '2',
                # '--lighthousecount', '2'
            ]
        ),

        # Composable launch
        ComposableNodeContainer(
            package='rclcpp_components',
            executable='component_container',
            name='libsurvive_ros2_container',
            composable_node_descriptions=[
                ComposableNode(
                    package='libsurvive_ros2',
                    plugin='libsurvive_ros2::Component',
                    name='libsurvive_ros2_component',
                    extra_arguments=[
                        {'use_intra_process_comms': True}
                    ]
                ),
                #
                # Add whatever other nodes you'd like here
                #
            ],
            output='log',
        ),
            
        # For bridging connection to foxglove running on a remote server.
        Node(
            package='rosbridge_server',
            executable='rosbridge_websocket',
            name='rosbridge_server_node',
            condition=IfCondition(LaunchConfiguration('rosbridge')),
            parameters=[
                {"port": 54321},
            ],
            output='log'
        ),
        Node(
            package='rosapi',
            executable='rosapi_node',
            name='rosapi_node',
            condition=IfCondition(LaunchConfiguration('rosbridge')),
            output='log'
        ),
        
        # For recording all data from the experiment
        ExecuteProcess(
            cmd=['ros2', 'bag', 'record', '-o', BAG_FILE] + [
                '/tf',
                '/tf_static'
            ],
            condition=IfCondition(LaunchConfiguration('record')),
            output='log'
        )
    ])