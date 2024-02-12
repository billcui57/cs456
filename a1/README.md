# Assignment 1
Bill Cui

b22cui

20818505
## Versions
Python 3.9.6

## Setup
Requirements are in `requirements.txt` file

You can generate files by using the `generate_files.py` script

By default both client and server will produce full logging output.
To reduce the amount of logging output, you can change the `LOG_LEVEL` variable in `client.py` and `server.py` to `logging.WARN` or above

Only IP addresses are supported in the command line

### Server
1. Create your own directory (e.g `mkdir storage`)
2. `chmod a+x server.sh`
3. `./server.sh <storage_path>`


### Client
1. `make clean-setup-client`
2. `chmod a+x client.sh`
3. `./client.sh <server_ip> <server_port> <command> <path>`

## Breakdown
- `client.py` is the main file for the client
- `server.py` is the main file for the server
- `custom_types.py` contains the custom types used between client and server
