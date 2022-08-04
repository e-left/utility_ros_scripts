from rosbags.rosbag2 import Reader, Writer
from rosbags.serde import deserialize_cdr, serialize_cdr
import sys


def remove_topics(src, dst, topics, tf):
    """Remove topic from rosbag2.

    Args:
        src: Source path.
        dst: Destination path.
        topic: Name of topic to remove.

    """
    with Reader(src) as reader, Writer(dst) as writer:
        conn_map = {}
        for conn in reader.connections.values():

            # remove any of the selected topics
            if conn.topic in topics:
                continue

            # write the valid message
            conn_map[conn.id] = writer.add_connection(
                conn.topic,
                conn.msgtype,
                conn.serialization_format,
                conn.offered_qos_profiles,
            )

        rconns = [reader.connections[x] for x in conn_map]
        for conn, timestamp, data in reader.messages(connections=rconns):
            # remove the selected TF pairs
            if conn.topic == "/tf":
                # we need to edit the TF
                # deserialize message
                msg = deserialize_cdr(data, conn.msgtype)

                # we need to remove the marked transforms, so we keep everything else
                msg.transforms = [transform for transform in msg.transforms for tfPair in tf if not (
                    transform.header.frame_id == tfPair[0] and transform.child_frame_id == tfPair[1])]

                data = serialize_cdr(msg, conn.msgtype)

            writer.write(conn_map[conn.id], timestamp, data)


topics = []
# [ [frame_id_1, child_frame_id_1], ...]
tf = []

if len(sys.argv) != 4:
    print("Incorrect number of arguments")
    print("Usage: python remove_topics.py <mode> <input_rosbag> <output_rosbag>")
    print("Where mode: odom")
    exit(1)

mode = sys.argv[1]
in_rosbag = sys.argv[2]
out_rosbag = sys.argv[3]

if mode == "odom":
    topics = ["/odom"]
    tf = [["odom", "base_link"]]

if mode == "fusion":
    topics = ["/fusion/insideBoundingBoxes", "/fusion/center_coneDistances",
              "/fusion/right_coneDistances", "/fusion/left_coneDistances"]

remove_topics(in_rosbag, out_rosbag, mode, tf)

print("Removed specified topics")
