import argparse
import math
import socket
import os
import logging
from custom_types import Request, GetRequestBody, Response

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)

logger = logging.getLogger('server')
BUF_SIZE = 1024


def main():
    parser = argparse.ArgumentParser(description='Server program.')
    parser.add_argument('storage',  type=str,
                        help='storage directory')
    args = parser.parse_args()

    HOST = socket.gethostname()
    STORAGE_DIR = args.storage

    logger.info("Server starting")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:

            udp_socket.bind((HOST, 0))
            server_n_port = udp_socket.getsockname()
            logger.info(f"Ready to receive on host {HOST} port {server_n_port}")
            while True:
                data,addr = udp_socket.recvfrom(BUF_SIZE)
                if not data:
                    break
                try:
                    request_json = data.decode('utf-8')
                    request = Request.from_json(request_json)
                except Exception as e:
                    logger.exception("Failed to unmarshal request")
                    break
                logger.info(request)

                if request.type == "GET":
                    get_request_body = GetRequestBody(**request.body)
                    logger.info("Handle Get Cmd")
                    logger.info(get_request_body)

                    down_file = os.path.join(STORAGE_DIR, get_request_body.file_name)

                    if not STORAGE_DIR or not os.path.isfile(down_file):
                        resp = Response(code=404, body={})
                        response_json = resp.to_json().encode("utf-8")
                        udp_socket.sendto(response_json, addr)
                    # If has file
                    else:
                        receive_port = get_request_body.receive_port
                        logger.info(f"Will be sending file to {addr[0]}:{receive_port}")

                        resp = Response(code=200, body={})
                        response_json = resp.to_json().encode("utf-8")
                        udp_socket.sendto(response_json,addr)

                        # transaction stage
                        logger.info("Transaction stage")
                        transaction_client_addr = (addr[0],receive_port)

                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
                            tcp_socket.connect(transaction_client_addr)
                            logger.info(f"Connected to {transaction_client_addr}")



                            file_size = os.path.getsize(down_file)
                            logger.info(f"File is of size {file_size} bytes")
                            logger.info(f"Sending file in chunks of size {BUF_SIZE}")
                            total_chunks = math.ceil(file_size/BUF_SIZE)

                            with open(down_file, 'rb') as output:
                                chunk_idx = 0
                                while True:
                                    data = output.read(BUF_SIZE)
                                    if not data:
                                        break
                                    tcp_socket.sendall(data)
                                    logger.info(f"Sent chunk {chunk_idx+1}/{total_chunks}")
                                    chunk_idx+=1
                            logger.info("Done sending")











if __name__ == "__main__":
    main()