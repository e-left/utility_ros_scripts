from rosbags.rosbag2 import Reader, Writer
import sys

def remove_topics(src, dst, topics):
    """Remove topic from rosbag2.

    Args:
        src: Source path.
        dst: Destination path.
        topic: Name of topic to remove.

    """
    with Reader(src) as reader, Writer(dst) as writer:
        conn_map = {}
        for conn in reader.connections.values():
            if conn.topic in topics:
                continue
            conn_map[conn.id] = writer.add_connection(
                conn.topic,
                conn.msgtype,
                conn.serialization_format,
                conn.offered_qos_profiles,
            )

        rconns = [reader.connections[x] for x in conn_map]
        for conn, timestamp, data in reader.messages(connections=rconns):
            writer.write(conn_map[conn.id], timestamp, data)

topics = []

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

remove_topics(in_rosbag, out_rosbag, mode)

print("Removed specified topics")