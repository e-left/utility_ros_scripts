#!/bin/bash

# $1: input rosbag
if [ $# -ne 1 ]
  then
    echo "Usage: ./visualize_graphs.sh <input_rosbag>"
    exit
fi

# run plotjuggler on data
ros2 run plotjuggler plotjuggler -d $1

wait -n
pkill -P $$
echo "Visualization completed successfully"