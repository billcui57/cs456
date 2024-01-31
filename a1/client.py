import argparse
import math
import os
import socket
import logging

from custom_types import Request, GetRequestBody, Response, PutRequestBody, PutResponseBody

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logger = logging.getLogger('client')

BUF_SIZE = 1024
DOWNLOAD_DIR = "download"
UPLOAD_DIR = "upload"

def get(file_name,server_address,server_n_port):
    HOST = socket.gethostname()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            tcp_socket.bind((HOST, 0))
            client_r_port = tcp_socket.getsockname()[1]
            tcp_socket.listen(5)
            logger.info(f"TCP socket is listening on {client_r_port}")

            request = Request(type="GET", body=GetRequestBody(receive_port=client_r_port, file_name=file_name).__dict__)
            udp_socket.sendto(request.to_json().encode("utf-8"), (server_address, server_n_port))

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
            conn,addr = tcp_socket.accept()
            logger.info(f"Got connection from {addr}")

            down_file = os.path.join(DOWNLOAD_DIR, file_name)

            with open(down_file, 'wb') as output:
                while True:
                    recieved_buffer = conn.recv(BUF_SIZE)
                    if not recieved_buffer:
                        break
                    output.write(recieved_buffer)
                    logger.info(f"Received chunk of size {len(recieved_buffer)} bytes")

            logger.info("Transfer complete")

def put(file_name,server_address,server_n_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:

        # negotiation stage
        request = Request(type="PUT", body=PutRequestBody( file_name=file_name).__dict__)
        udp_socket.sendto(request.to_json().encode("utf-8"), (server_address, server_n_port))
        data, _ = udp_socket.recvfrom(BUF_SIZE)
        logger.info("Got response from server")
        response_json = data.decode('utf-8')
        response = Response.from_json(response_json)
        put_response_body = PutResponseBody(**response.body)

        server_receive_port = put_response_body.receive_port
        logger.info(response)

        # transaction stage
        logger.info("Transaction stage")
        transaction_server_addr = (server_address, server_receive_port)

        upload_file = os.path.join(UPLOAD_DIR, file_name)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            tcp_socket.connect(transaction_server_addr)
            logger.info(f"Connected to {transaction_server_addr}")

            file_size = os.path.getsize(upload_file)
            logger.info(f"File is of size {file_size} bytes")
            logger.info(f"Sending file in chunks of size {BUF_SIZE}")
            total_chunks = math.ceil(file_size / BUF_SIZE)

            with open(upload_file, 'rb') as output:
                chunk_idx = 0
                while True:
                    data = output.read(BUF_SIZE)
                    if not data:
                        break
                    tcp_socket.sendall(data)
                    logger.info(f"Sent chunk {chunk_idx + 1}/{total_chunks}")
                    chunk_idx += 1
            logger.info("Done sending")





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

    file_name = args.filename
    server_address = args.server_address
    server_n_port = args.n_port

    try:
        if args.command == "GET":
            get(file_name,server_address,server_n_port)
        elif args.command == "PUT":
            put(file_name,server_address,server_n_port)
        else:
            logger.warning("Invalid command")
    except Exception:
        logger.exception("Client bad")











if __name__ == "__main__":
    main()