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
    print v['MAC']
    dt1 = v['T2'] - v['T1']
    dt2 = v['T4'] - v['T3']
    print dt1, dt2