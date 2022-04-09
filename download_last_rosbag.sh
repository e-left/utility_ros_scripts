ROSBAG_PATH=$(ssh apu ls /home/talos-apu/rosbag_db/ | tail -n 1)
scp -r apu:/home/talos-apu/rosbag_db/$ROSBAG_PATH .
