'''
kyochon_info_db.py
'''

import MySQLdb

# 데이터베이스 연결

# conn = MySQLdb.connect(
#     host='', port=, database='',
#     user='', password=''
# )

cursor = conn.cursor()
print("디비연결 성공")


import csv
filename = 'kyochon_info.csv'
file = csv.reader(open(filename, 'r', encoding='utf-8'), delimiter=';')

for row in file:
    sql = '''
        INSERT INTO kyochoninfo (city, county, district, address, tel)
        VALUES (%s, %s, %s, %s, %s)
    '''
    cursor.execute(sql, row)

conn.commit()
conn.close()