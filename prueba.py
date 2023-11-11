import pyshark
import psutil

# Define a function to get non-loopback network interfaces
def get_non_loopback_interfaces():
    interfaces = psutil.net_if_stats()
    non_loopback_interfaces = [iface for iface in interfaces if not iface.startswith('lo')]
    return non_loopback_interfaces

# Define a function to capture TCP traffic and collect the required data
def capture_tcp_traffic():
    capture_filter = "tcp"
    non_loopback_interfaces = get_non_loopback_interfaces()

    for interface_name in non_loopback_interfaces:
        capture = pyshark.LiveCapture(interface=interface_name, display_filter=capture_filter)
        transmitted_bytes = 0
        received_bytes = 0
        forward_packets = 0
        backward_packets = 0
        for packet in capture.sniff_continuously():
            try:
                # Check if the packet has a 'tcp' layer
                if 'TCP' in packet:
                    tcp = packet['TCP']
                    ip = packet['IP']

                    # Check if it's a forward packet (from source to destination)
                    if int(tcp.seq) > int(tcp.ack):
                        transmitted_bytes += float(tcp.len)
                        forward_packets += 1
                        source_ip = ip.src
                        source_port = tcp.srcport
                        dest_ip = ip.dst
                        dest_port = tcp.dstport
                        print(f"Transmitted bytes: {transmitted_bytes} | Source: {source_ip}:{source_port} -> Destination: {dest_ip}:{dest_port}")

                    # Check if it's a backward packet (from destination to source)
                    else:
                        received_bytes += float(tcp.len)
                        backward_packets += 1
                        source_ip = ip.src
                        source_port = tcp.srcport
                        dest_ip = ip.dst
                        dest_port = tcp.dstport
                        print(f"Received bytes: {received_bytes} | Source: {source_ip}:{source_port} -> Destination: {dest_ip}:{dest_port}")

            except KeyError:
                pass  # Some packets may not have a TCP layer

# Usage
if __name__ == "__main__":
    capture_tcp_traffic()
