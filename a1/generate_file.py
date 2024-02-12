import os

GB1 = 1024*1024*1024 # 1GB
size = 1 # desired size in GB
with open('bigfile.txt', 'wb') as fout:
    for i in range(size + 1):
        fout.write(os.urandom(GB1))