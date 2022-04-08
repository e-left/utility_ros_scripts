#!/bin/bash

# $1: input rosbag
if [ $# -ne 1 ]
  then
    echo "Usage: ./visualize_run.sh <input_rosbag>"
    exit
fi

# run rviz
ros2 run rviz2 rviz2 &

# wait a bit
sleep 5

# play the rosbag
ros2 bag play $1 &

wait -n
pkill -P $$
echo "Visualization completed successfully"