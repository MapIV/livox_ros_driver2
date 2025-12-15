import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import EnvironmentVariable
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
import launch

################### user configure parameters for ros2 start ###################
xfer_format   = 0
multi_topic   = 0
data_src      = 0
publish_freq  = 10.0
output_type   = 0
frame_id      = 'mid360/livox_frame' # 静的なframe_idを定義
lvx_file_path = '/home/livox/livox_test.lvx'
cmdline_bd_code = 'livox47MCN7J0032590'

cur_path = os.path.split(os.path.realpath(__file__))[0] + '/'
cur_config_path = cur_path + '../config'
rviz_config_path = os.path.join(cur_config_path, 'display_point_cloud_ROS2.rviz')
user_config_path = os.path.join(cur_config_path, 'MID360_config.json')
################### user configure parameters for ros2 end #####################

# 変更点 1: パラメータを単一の辞書として定義し直す
livox_ros2_params = {
    "xfer_format": xfer_format,
    "multi_topic": multi_topic,
    "data_src": data_src,
    "publish_freq": publish_freq,
    "output_data_type": output_type,
    "frame_id": frame_id,
    "lvx_file_path": lvx_file_path,
    "user_config_path": user_config_path,
    "cmdline_input_bd_code": cmdline_bd_code
}


def generate_launch_description():

    # ROS_NAMESPACEを取得
    namespace = EnvironmentVariable('ROS_NAMESPACE', default_value='')

    # 変更点 2: frame_idを動的に構築し、辞書内の値を上書きする
    # namespaceとframe_idを'/'で結合する
    livox_ros2_params['frame_id'] = PathJoinSubstitution([
        namespace, # EnvironmentVariableオブジェクト
        frame_id   # 静的文字列
    ])

    livox_driver = Node(
        package='livox_ros_driver2',
        executable='livox_ros_driver2_node',
        name='livox_lidar_publisher',
        namespace=namespace,
        remappings=[
            ('livox/lidar', 'livox/mid360/lidar'),
            ('livox/imu', 'livox/mid360/imu'),
        ],
        output='screen',
        # 変更点 3: パラメータ辞書をリストでラップして渡す
        parameters=[livox_ros2_params] 
        )

    livox_rviz = Node(
            package='rviz2',
            executable='rviz2',
            namespace=namespace,
            output='screen',
            arguments=['--display-config', rviz_config_path]
        )

    return LaunchDescription([
        livox_driver,
        livox_rviz,
    ])