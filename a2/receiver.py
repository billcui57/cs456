import argparse
import math
import socket
import os
import logging
from packet import Packet


logging.basicConfig()
logging.root.setLevel(logging.INFO)

logger = logging.getLogger('receiver')

BURST_SIZE = 10
PACKET_SIZE = 500
BUFFER_SIZE = 2048

def main():
    parser = argparse.ArgumentParser(description='Receiver program.')
    parser.add_argument("emulator_host", type=str,help="Host address of the emulator")
    parser.add_argument("emulator_udp_port", type=int,help="UDP port of the emulator")
    parser.add_argument("receiver_udp_port", type=int,help="UDP port of the receiver")
    parser.add_argument("file", type=str,help="Filename to write to")
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind(("", args.receiver_udp_port))


        with open(args.file, 'w') as output:
            while True:
                received_buffer, _ = udp_socket.recvfrom(BUFFER_SIZE)
                type, seq_num, length, data = Packet(received_buffer).decode()

                # EOT
                if type == 2:
                    break

                output.write(data)
                logger.info(f"Received seq num {seq_num} chunk of length {length}")

        logger.info("Done receiving")


















if __name__ == "__main__":
    main()