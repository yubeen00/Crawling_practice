from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

#Chrome 옵션
options = webdriver.ChromeOptions()

driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome('./webdriver/chromedriver.exe')

#implicitly_wait - 브라우저 대기
driver.implicitly_wait(5)

driver.get('http://www.kyochon.com/shop/domestic.asp')

wait = WebDriverWait(driver, 10)

# 시/도 드롭다운 선택
sido_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, 'sido1'))))
sido_values = list(range(1, 6))
	## EC.presence_of_element_located - WebDriver의 기능 중 하나
		# 특정 요소가 웹 페이지에 나타날 때까지 기다리는 조건을 정의함
			# 위 코드에서는 By.ID와 sido1을 사용하여 id가 'sido1'인 요소가 나타날 때까지 기다림.
	## wait.until() - WebDriver를 특정 조건이 충족될 때까지 기다리는 기능 제공
	## Select() - Selenium의 Select클래스의 인스턴스를 만듦. HTML요소를 다루는데 사용

# 대기 설정
wait = WebDriverWait(driver, 10)

# 시/도 반복
for sido_value in sido_values:
    # 시/도 선택
    sido_dropdown.select_by_value(str(sido_value))
	    ## select_by_value() - 특정 값 선택
		    # sido_dropdown.select_by_value(str(sido_value)) - 드롭다운 메뉴에서 문자열로 변환된 'sido_value'에 해당하는 값 선택

    # 대기: 시/군/구 옵션 로딩을 기다림
    wait.until(EC.presence_of_element_located((By.ID, 'sido2')))

    # 시/군/구 옵션 가져오기
    sigungu_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, 'sido2'))))


    # 시/군/구 반복
    for i in range(len(sigungu_dropdown.options)):
        # 시/군/구를 선택할 때마다 sigungu_dropdown을 다시 찾기
        sigungu_dropdown = Select(driver.find_element(By.ID, 'sido2'))
        sigungu_dropdown.select_by_index(i)

        # 검색 버튼 클릭
        search_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'faqSchBtn')))
        search_button.click()
		        ## EC.element_to_be_clickable - 특정 요소가 클릭 가능한 상태의 조건 정의

        # 대기: 검색 결과가 나타날 때까지
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.list li')))

        # 다시 요소 참조
        sido_dropdown = Select(driver.find_element(By.ID, 'sido1'))
        sigungu_dropdown = Select(driver.find_element(By.ID, 'sido2'))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        store_items = soup.select('ul.list li')

        # 각 매장 정보 출력
        for item in store_items:
            # select_one 결과가 None이 아닌지 확인
            store_name_element = item.select_one('span.store_item strong')
            if store_name_element:
                store_name = store_name_element.text.strip()
                address_lines = list(item.select_one('span.store_item em').stripped_strings)
                address = ''.join(address_lines[0])
                tel = item.select_one('span.store_item em').contents[-1].strip()

                # 정규표현식을 사용하여 주소에서 필요한 부분만 추출
                address_pattern = re.compile(r'(.+ \d+-\d+)')
                match = address_pattern.search(address)
                if match:
                    address = match.group(1)

                # 파일에 쓰기
                with open('kyochon_info.csv', 'a', encoding='utf-8') as file:
                    file.write(f"{sido_dropdown.first_selected_option.text}; {sigungu_dropdown.options[i].text}; {store_name}; {address}; {tel}\n")

# 브라우저 종료
driver.quit()
