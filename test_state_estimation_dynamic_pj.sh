#!/bin/bash

# $1: input rosbag
if [ $# -ne 1 ]
  then
    echo "Usage: ./test_state_estimation_dynamic.sh <input_rosbag>"
    exit
fi

# create test data here
python3 /home/eleft/utility_ros_scripts/remove_topics.py odom $1 tmp_ros

# run state_estimation or state_estimation+slam node based on input
ros2 launch turtle_estimation state_estimation.launch.xml &

# run rviz
ros2 run plotjuggler plotjuggler &

# ensure node and pj start up, give some more time to set up pj
sleep 10

# play processed rosbag
ros2 bag play tmp_ros &

wait -n
pkill -P $$
echo "Test completed successfully"
rm -rf tmp_ros
