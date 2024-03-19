import folium
import MySQLdb

def display_map():
    # 데이터베이스 연결
    # conn = MySQLdb.connect(host='',
    #                        port=,
    #                        database='',
    #                        user='',
    #                        password='')
    cursor = conn.cursor()
    print("디비연결 성공")

    # 데이터베이스에서 위도와 경도 가져오기
    cursor.execute('SELECT latitude, longitude, address FROM kyochoninfo WHERE latitude IS NOT NULL AND longitude IS NOT NULL')
    rows = cursor.fetchall() #  모든 결과 가져오기

    # Folium 지도 생성
    a = folium.Map(location=[37.5, 127], zoom_start=12)

    # 데이터베이스에서 가져온 위치에 마커 추가
    for row in rows:
        lat, lon, address = row
        folium.Marker(location=[float(lat), float(lon)], popup=address).add_to(a)

    # 지도 저장
    a.save('C:\\Users\\user\\Desktop\\프로젝트\\웹 크롤링\\Chicken_crawling\\custom_map.html')

    # 연결 닫기
    conn.close()

if __name__ == "__main__":
    display_map()
