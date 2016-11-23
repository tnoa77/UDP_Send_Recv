import os

total_count = 20
for i in range(0, total_count):
    print i, "of", total_count
    os.system("python icmp.py > /dev/null 2>&1")
