import MySQLdb
import requests

def get_lat_lng(address):
    base_url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': address,
        'format': 'jsonv2'
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data:
            lat, lon = str(data[0]['lat']), str(data[0]['lon'])
            return lat, lon
    return None, None

def update_lat_lng():
    # 데이터베이스 정보 입력하기
    
    # conn = MySQLdb.connect(host='',
    #                        port=,
    #                        database='',
    #                        user='',
    #                        password='')
    cursor = conn.cursor()

    cursor.execute('SELECT address FROM kyochoninfo WHERE latitude IS NULL AND longitude IS NULL')
    rows = cursor.fetchall()

    for address_row in rows:
        address = address_row[0]
        lat, lon = get_lat_lng(address)
        if lat is not None and lon is not None:
            cursor.execute('UPDATE kyochoninfo SET latitude=%s, longitude=%s WHERE address=%s', (lat, lon, address))
            print(f"주소 {address}가 업데이트 되었습니다.")

    conn.commit()
    conn.close()

    print("업데이트가 완료되었습니다.")

if __name__ == "__main__":
    update_lat_lng()
