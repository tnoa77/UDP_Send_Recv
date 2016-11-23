import os
from MySQL import *
db = MySQL()

# total_count = 20
# for i in range(0, total_count):
#     print (i + 1), "of", total_count
#     os.system("python icmp.py > /dev/null 2>&1")

sql = "SELECT * FROM kw_icmp"
rel = db.query(sql)

for v in rel:
    print v[1]
    dt1 = v[3] - v[2]
    dt2 = v[5] - v[4]
    print dt1, dt2