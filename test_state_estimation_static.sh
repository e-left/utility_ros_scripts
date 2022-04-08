#!/bin/bash

# $1: input rosbag
# $2: output rosbag
if [ $# -ne 2 ]
  then
    echo "Usage: ./test_state_estimation_static.sh <input_rosbag> <output_rosbag>"
    exit
fi

# create test data here
python3 /home/eleft/utility_ros_scripts/remove_topics.py odom $1 tmp_ros

# record output data
ros2 bag record -a -o $2 &

# run state_estimation or state_estimation+slam node based on input
ros2 launch turtle_estimation state_estimation.launch.xml &

# ensure node starts up
sleep 3

# play processed rosbag
ros2 bag play tmp_ros &

wait -n
pkill -P $$
echo "Test completed successfully"
rm -rf tmp_ros