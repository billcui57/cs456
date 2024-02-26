import os
import random

KB1 = 1024  # 1KB
size_kb = 100  # desired size in KB

# Function to generate a string of valid ASCII characters
def generate_ascii_chars(num_chars):
    return ''.join(chr(random.randint(32, 126)) for _ in range(num_chars))

with open('to.txt', 'w') as fout:
    for _ in range(size_kb):
        # Generate and write 1KB of ASCII characters
        fout.write(generate_ascii_chars(KB1))
