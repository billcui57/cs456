import argparse
import os
import socket
import logging

from custom_types import Request, GetRequestBody, Response

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logger = logging.getLogger('client')

BUF_SIZE = 1024
DOWNLOAD_DIR = "download"
SERVER_ADDRESS = ""
SERVER_N_PORT = 0


def get():
    HOST = socket.gethostname()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            tcp_socket.bind((HOST, 0))
            client_r_port = tcp_socket.getsockname()[1]
            request = Request(type="GET", body=GetRequestBody(receive_port=client_r_port, file_name=FILE_NAME).__dict__)
            udp_socket.sendto(request.to_json().encode("utf-8"), (SERVER_ADDRESS, SERVER_N_PORT))

            # negotiation stage
            data, server = udp_socket.recvfrom(BUF_SIZE)
            logger.info("Got response from server")

            response_json = data.decode('utf-8')
            response = Response.from_json(response_json)
            logger.info(response)

            if response.code == 404:
                logger.warning("Not found")
                return
            elif response.code == 200:
                logger.info("Ok")
            else:
                logger.warning("Invalid response code")
                return

            # transaction stage
            logger.info("Transaction stage")
            tcp_socket.listen(5)
            logger.info(f"TCP socket is listening on {client_r_port}")
            conn,addr = tcp_socket.accept()
            logger.info(f"Got connection from {addr}")

            down_file = os.path.join(DOWNLOAD_DIR, FILE_NAME)

            with open(down_file, 'wb') as output:
                while True:
                    recieved_buffer = conn.recv(BUF_SIZE)
                    if not recieved_buffer:
                        break
                    output.write(recieved_buffer)
                    logger.info(f"Received chunk of size {len(recieved_buffer)} bytes")

            logger.info("Transfer complete")


def main():
    parser = argparse.ArgumentParser(description='Client program.')
    parser.add_argument('server_address',  type=str,
                        help='address of server')
    parser.add_argument('n_port',  type=int,
                        help='negotiation port')
    parser.add_argument('command', type=str, help="command to do")
    parser.add_argument('filename', type=str, help="file to get or put")
    args = parser.parse_args()

    logger.info("Client starting")

    global FILE_NAME
    global SERVER_N_PORT
    global SERVER_ADDRESS
    FILE_NAME = args.filename
    SERVER_ADDRESS = args.server_address
    SERVER_N_PORT = args.n_port

    if args.command == "GET":
        get()











if __name__ == "__main__":
    main()