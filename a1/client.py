import argparse
import socket
import logging

from custom_types import Request, GetRequestBody, Response

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logger = logging.getLogger('client')
def main():
    parser = argparse.ArgumentParser(description='Client program.')
    parser.add_argument('server_address',  type=str,
                        help='address of server')
    parser.add_argument('n_port',  type=int,
                        help='negotiation port')
    args = parser.parse_args()

    logger.info("Client starting")
    HOST = "127.0.0.1"

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            tcp_socket.bind((HOST, 0))
            client_r_port = tcp_socket.getsockname()[1]


            request = Request(type="GET", body=GetRequestBody(receive_port=client_r_port, file_name="hey").__dict__)
            udp_socket.sendto(request.to_json().encode("utf-8"), (args.server_address, args.n_port))

            # negotiation stage
            data, server = udp_socket.recvfrom(1024)
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
            while True:
                conn,addr = tcp_socket.accept()
                logger.info(f"Got connection from {addr}")







if __name__ == "__main__":
    main()