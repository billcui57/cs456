import argparse
import math
import socket
import os
import logging
import time

from packet import Packet


logging.basicConfig()
logging.root.setLevel(logging.INFO)

logger = logging.getLogger('sender')

BURST_SIZE = 10
PACKET_SIZE = 500
BUFFER_SIZE = 2048

def main():
    parser = argparse.ArgumentParser(description='Sender program.')
    parser.add_argument("emulator_host", type=str,help="Host address of the emulator")
    parser.add_argument("emulator_udp_port", type=int,help="UDP port of the emulator")
    parser.add_argument("sender_udp_port", type=int,help="UDP port of the sender")
    parser.add_argument("timeout", type=int,help="Timeout in milliseconds")
    parser.add_argument("file", type=str,help="File to send")
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.settimeout(args.timeout/1000)
        udp_socket.bind(("", args.sender_udp_port))

        file_size = os.path.getsize(args.file)
        logger.info(f"File is of size {file_size} bytes(chars)")
        logger.info(f"Sending file in chunks of size {PACKET_SIZE} chars")


        seq_num = 0

        emulator_addr = (args.emulator_host,args.emulator_udp_port)

        done_transmitting = False

        with open(args.file, 'r') as output:
            while not done_transmitting:
                logger.info(f"Beginning burst")
                packets_sent = dict()
                seq_nums_waiting_ack = set()
                for i in range(BURST_SIZE):
                    data = output.read(PACKET_SIZE)
                    if not data:
                        done_transmitting = True
                        break
                    packet = Packet(1, seq_num, len(data), data)
                    udp_socket.sendto(packet.encode(), emulator_addr)

                    packets_sent[seq_num] = packet
                    seq_nums_waiting_ack.add(seq_num)

                    logger.info(f"Sent seq num {seq_num}")
                    seq_num += 1

                while len(seq_nums_waiting_ack) > 0:
                    logger.info("Waiting for acks")
                    # get acks
                    try:
                        received_buffer, _ = udp_socket.recvfrom(BUFFER_SIZE)
                        type, seq_num, length, data = Packet(received_buffer).decode()
                        if type != 0:
                            logger.error("Not supposed to get anything other than an ack")
                        logger.info(f"Got ack for seq num {seq_num}")

                        if seq_num in seq_nums_waiting_ack:
                            seq_nums_waiting_ack.remove(seq_num)
                    except socket.timeout:
                        logger.info("Could not get acks back in time")
                    # retransmitting
                    for seq_num in seq_nums_waiting_ack:
                        udp_socket.sendto(packets_sent[seq_num].encode(), emulator_addr)
                        logger.info(f"Resending seq num {seq_num}")




        logger.info("Done sending")

        packet = Packet(2, seq_num, 0, "")
        udp_socket.sendto(packet.encode(), emulator_addr)


        logger.info("Waiting on EOT")
        while True:
            received_buffer, _ = udp_socket.recvfrom(BUFFER_SIZE)
            type, seq_num, length, data = Packet(received_buffer).decode()
            if type == 2:
                break






















if __name__ == "__main__":
    main()