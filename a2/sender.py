import argparse
import math
import socket
import os
import logging
from packet import Packet


logging.basicConfig()
logging.root.setLevel(logging.INFO)

logger = logging.getLogger('sender')

BURST_SIZE = 10
PACKET_SIZE = 500

def main():
    parser = argparse.ArgumentParser(description='Sender program.')
    parser.add_argument("emulator_host", type=str,help="Host address of the emulator")
    parser.add_argument("emulator_udp_port", type=int,help="UDP port of the emulator")
    parser.add_argument("sender_udp_port", type=int,help="UDP port of the sender")
    parser.add_argument("timeout", type=int,help="Timeout in milliseconds")
    parser.add_argument("file", type=str,help="File to send")
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind(("", args.sender_udp_port))

        file_size = os.path.getsize(args.file)
        logger.info(f"File is of size {file_size} bytes(chars)")
        logger.info(f"Sending file in chunks of size {PACKET_SIZE} chars")

        seq_num = 0

        emulator_addr = (args.emulator_host,args.emulator_udp_port)

        with open(args.file, 'r') as output:
            while True:
                data = output.read(PACKET_SIZE)
                if not data:
                    break
                packet = Packet(1, seq_num, len(data), data)
                udp_socket.sendto(packet.encode(), emulator_addr)
                logger.info(f"Sent seq num {seq_num}")
                seq_num += 1
        packet = Packet(2, seq_num, 0, "")
        udp_socket.sendto(packet.encode(), emulator_addr)

        logger.info("Done sending")



















if __name__ == "__main__":
    main()