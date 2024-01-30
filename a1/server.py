import socket
from dotenv import load_dotenv
import os
import logging
from custom_types import Request, GetRequestBody, Response

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)


logger = logging.getLogger('server')






def main():
    load_dotenv()
    HOST = os.getenv("SERVER_HOST")

    logger.info("Server starting")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            udp_socket.bind((HOST, 0))
            server_n_port = udp_socket.getsockname()
            logger.info(f"Ready to receive on host {HOST} port {server_n_port}")
            while True:
                data,addr = udp_socket.recvfrom(1024)
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

                    # If has file
                    if True:
                        receive_port = get_request_body.receive_port
                        logger.info(f"Will be sending file to {addr[0]}:{receive_port}")

                        resp = Response(code=200, body={})
                        response_json = resp.to_json().encode("utf-8")
                        udp_socket.sendto(response_json,addr)

                        # transaction stage
                        logger.info("Transaction stage")
                        transaction_client_addr = (addr[0],receive_port)

                        tcp_socket.connect(transaction_client_addr)
                        logger.info(f"Connected to {transaction_client_addr}")
                    else:
                        resp = Response(code=200, body={})
                        response_json = resp.to_json().encode("utf-8")
                        udp_socket.sendto(response_json, addr)









if __name__ == "__main__":
    main()