import os
from MySQL import *
db = MySQL()

# total_count = 20
# for i in range(0, total_count):
#     print (i + 1), "of", total_count
#     os.system("python icmp.py > /dev/null 2>&1")

sql = "SELECT * FROM kw_icmp"
rel = db.query(sql)

f = open('test.in', "wb")
for v in rel:
    dt1 = v[3] - v[2]
    dt2 = v[5] - v[4]
    f.write("1 1:" + dt1 + "\n")
    f.write("0 1:" + dt1 + "\n")
f.close()