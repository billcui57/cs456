# Assignment 2
Bill Cui

b22cui

20818505
## Versions
Python 3.9.6

## Setup
Requirements are in `requirements.txt` file

You can generate a text file of 100kb by using the `generate_file.py` script. Feel free to modify `size_kb` to change the size of the file you want.

By default both sender and receiver will produce full logging output.
To reduce the amount of logging output, you can change the `LOG_LEVEL` variable in `sender.py` and `receiver.py` to `logging.WARN` or above

I have a utility script `generate_run_commands.sh` that should create run commands for sender receiver and emulator with free ports. You may use that as a starting point to save time finding which ports are free.
