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

        emulator_addr = (args.emulator_host,args.emulator_udp_port)

        udp_socket.bind(("", args.receiver_udp_port))

        packet_buffer = dict()
        expected_seq_num = 0
        with open(args.file, 'w') as output:
            while True:
                received_buffer, _ = udp_socket.recvfrom(BUFFER_SIZE)
                type, seq_num, length, data = Packet(received_buffer).decode()

                # EOT
                if type == 2:
                    break

                logger.info(f"Received seq num {seq_num} chunk of length {length}")
                if seq_num in packet_buffer:
                    logger.info(f"Seq num {seq_num} was a duplicate")

                packet_buffer[seq_num] = data

                logger.info(f"Replying ack")
                ack_packet = Packet(0, seq_num, 0, "")
                udp_socket.sendto(ack_packet.encode(), emulator_addr)

                while expected_seq_num in packet_buffer:
                    logger.info(f"Writing seq num {expected_seq_num} to disk")
                    output.write(packet_buffer[expected_seq_num])
                    expected_seq_num += 1


        logger.info("Done receiving")

        packet = Packet(2, seq_num, 0, "")
        udp_socket.sendto(packet.encode(), emulator_addr)

        logger.info("Sent EOT")

















if __name__ == "__main__":
    main()