import argparse
import math
import socket
import os
import logging
from custom_types import Request, GetRequestBody, Response, PutRequestBody, PutResponseBody

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)

logger = logging.getLogger('server')
BUF_SIZE = 1024


def handle_get(s,addr,get_request_body,storage_dir):
    logger.info("Handle Get Cmd")
    logger.info(get_request_body)

    # negotiation stage
    down_file = os.path.join(storage_dir, get_request_body.file_name)

    if not storage_dir or not os.path.isfile(down_file):
        resp = Response(code=404, body={})
        response_json = resp.to_json().encode("utf-8")
        s.sendto(response_json, addr)
        return

    receive_port = get_request_body.receive_port
    logger.info(f"Will be sending file to {addr[0]}:{receive_port}")

    resp = Response(code=200, body={})
    response_json = resp.to_json().encode("utf-8")
    s.sendto(response_json, addr)

    # transaction stage
    logger.info("Transaction stage")
    transaction_client_addr = (addr[0], receive_port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.connect(transaction_client_addr)
        logger.info(f"Connected to {transaction_client_addr}")

        file_size = os.path.getsize(down_file)
        logger.info(f"File is of size {file_size} bytes")
        logger.info(f"Sending file in chunks of size {BUF_SIZE}")
        total_chunks = math.ceil(file_size / BUF_SIZE)

        with open(down_file, 'rb') as output:
            chunk_idx = 0
            while True:
                data = output.read(BUF_SIZE)
                if not data:
                    break
                tcp_socket.sendall(data)
                logger.info(f"Sent chunk {chunk_idx + 1}/{total_chunks}")
                chunk_idx += 1
        logger.info("Done sending")

def handle_put(s,addr,put_request_body,storage_dir):
    logger.info("Handle Put Cmd")
    logger.info(put_request_body)

    HOST = socket.gethostbyname(socket.gethostname())

    # negotiation stage
    upload_file = os.path.join(storage_dir, put_request_body.file_name)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.bind((HOST,0))
        server_receive_port = tcp_socket.getsockname()[1]
        logger.info(f"Ready to receive file on port {tcp_socket.getsockname()}")
        response_body = PutResponseBody(receive_port=server_receive_port)
        resp = Response(code=200, body=response_body.__dict__)
        response_json = resp.to_json().encode("utf-8")
        s.sendto(response_json, addr)

        # transaction stage
        logger.info("Transaction stage")
        tcp_socket.listen(5)
        conn, addr = tcp_socket.accept()
        logger.info(f"Got connection from {addr}")

        with open(upload_file, 'wb') as output:
            while True:
                recieved_buffer = conn.recv(BUF_SIZE)
                if not recieved_buffer:
                    break
                output.write(recieved_buffer)
                logger.info(f"Received chunk of size {len(recieved_buffer)} bytes")

        logger.info("Transfer complete")



def main():
    parser = argparse.ArgumentParser(description='Server program.')
    parser.add_argument('storage',  type=str,
                        help='storage directory')
    args = parser.parse_args()

    HOST = socket.gethostbyname(socket.gethostname())

    storage_dir = args.storage

    logger.info("Server starting")
    logger.info(f"Server host {HOST}")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:

            udp_socket.bind((HOST, 0))
            logger.info(f"Ready to receive on {udp_socket.getsockname()}")
            while True:
                try:
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
                        handle_get(udp_socket,addr,get_request_body,storage_dir)
                    elif request.type == "PUT":
                        put_request_body = PutRequestBody(**request.body)
                        handle_put(udp_socket,addr,put_request_body,storage_dir)
                    else:
                        resp = Response(code=400, body={})
                        response_json = resp.to_json().encode("utf-8")
                        udp_socket.sendto(response_json, addr)
                except Exception:
                    logger.exception("Could not service")












if __name__ == "__main__":
    main()