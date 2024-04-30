import os

from ament_index_python import get_package_share_directory
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument,IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    res = []

    port_launch_arg = DeclareLaunchArgument(
        name="port",
        default_value="/dev/ttyUSB0"
    )
    res.append(port_launch_arg)

    baud_launch_arg = DeclareLaunchArgument(
        name="baud",
        default_value="115200"
    )
    res.append(baud_launch_arg)

    model_launch_arg = DeclareLaunchArgument(
        name="model",
        default_value=os.path.join(
            get_package_share_directory("mycobot_description"),
            "urdf/mycobot_320_m5_2022/mycobot_320_m5_2022.urdf"
        )
    )
    res.append(model_launch_arg)

    rvizconfig_launch_arg = DeclareLaunchArgument(
        name="rvizconfig",
        default_value=os.path.join(
            get_package_share_directory("mycobot_320"),
            "config/mycobot_pro_320.rviz"
        )
    )
    res.append(rvizconfig_launch_arg)

    num_launch_arg = DeclareLaunchArgument(
        name="num",
        default_value="0",
    )
    res.append(num_launch_arg)

    robot_description = ParameterValue(
        Command(
            [
                'xacro ',
                LaunchConfiguration('model')
            ]
        ),
        value_type=str
    )

    robot_state_publisher_node = Node(
        name="robot_state_publisher",
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}],
        arguments=[LaunchConfiguration("model")]
    )
    res.append(robot_state_publisher_node)
    
    cam_topic_cmd = DeclareLaunchArgument(
        "input_image_topic",
        default_value="/camera2/image_raw",
        description="Name of the input image topic",
        )
    res.append(cam_topic_cmd)
    usb_cam_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([FindPackageShare("usb_cam"), '/launch/camera.launch.py']),
        )
    res.append(usb_cam_cmd)

    cube_tf_node = Node(
        name="pickandplace",
        package="pickandplace",
        executable="cube",
        parameters=[{'input_image_topic' : LaunchConfiguration("input_image_topic")}]
    )
    res.append(cube_tf_node)

    follow_display_node = Node(
        name="follow_display",
        package="mycobot_320",
        executable="follow_display",
    )
    res.append(follow_display_node)

    rviz_node = Node(
        name="rviz2",
        package="rviz2",
        executable="rviz2",
        # output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')]
    )
    res.append(rviz_node)
    
    real_listener_node = Node(
        name="listen_real_of_topic",
        package="mycobot_320",
        executable="listen_real_of_topic"
    )
    res.append(real_listener_node)

    return LaunchDescription(res)
