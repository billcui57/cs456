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

POOL_SIZE = 10
PACKET_SIZE = 500
BUFFER_SIZE = 2048

SEQNUM_LOG_FILE = "seqnum.log"
ACK_LOG_FILE = "ack.log"

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

        seq_num = 0

        send_pool = dict()

        done_sending = False
        emulator_addr = (args.emulator_host,args.emulator_udp_port)


        with open(args.file, 'r') as output, open(SEQNUM_LOG_FILE, "w") as seqnum_log, open(ACK_LOG_FILE,"w") as ack_log:

            while True:

                while len(send_pool.keys()) < POOL_SIZE:
                    data = output.read(PACKET_SIZE)
                    if not data:
                        done_sending = True
                        break
                    packet = Packet(1, seq_num, len(data), data)
                    udp_socket.sendto(packet.encode(), emulator_addr)


                    seqnum_log.write(f"{seq_num}\n")

                    send_pool[seq_num] = packet
                    logger.info(f"Sent seq num {seq_num}")
                    seq_num += 1

                logger.info(f"Send pool: {list(send_pool.keys())}")

                if len(send_pool.keys()) > 0:
                    logger.info("Waiting for acks")
                    # get acks
                    try:
                        while True:
                            received_buffer, _ = udp_socket.recvfrom(BUFFER_SIZE)
                            type, ack_seq_num, length, data = Packet(received_buffer).decode()
                            if type != 0:
                                logger.error("Not supposed to get anything other than an ack")
                            logger.info(f"Got ack for seq num {ack_seq_num}")

                            if ack_seq_num in send_pool:
                                send_pool.pop(ack_seq_num, 0)


                            ack_log.write(f"{ack_seq_num}\n")
                    except socket.timeout:
                        logger.info("Timeout")
                        for resend_seq_num, resend_packet in send_pool.items():
                            logger.info(f"Resending seq num {resend_seq_num}")
                            udp_socket.sendto(resend_packet.encode(), emulator_addr)
                            seqnum_log.write(f"{resend_seq_num}\n")
                if len(send_pool.keys()) == 0 and done_sending:
                    break



        logger.info("Done sending")

        packet = Packet(2, seq_num, 0, "")
        udp_socket.sendto(packet.encode(), emulator_addr)


        logger.info("Waiting on EOT")
        while True:
            received_buffer, _ = udp_socket.recvfrom(BUFFER_SIZE)
            type, seq_num, length, data = Packet(received_buffer).decode()
            if type == 2:
                with open(ACK_LOG_FILE, "a") as log_file:
                    log_file.write("EOT\n")
                break









if __name__ == "__main__":
    main()