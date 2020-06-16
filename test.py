import sys, requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
sys.path.insert(0, './src/')
out_dir = './data/h_desc/'
# Importing local scripts


####################
# add logger later #
####################

# Chrome driver setup (running chome in headless mode)
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
DRIVER_PATH = './chromedriver/chromedriver'
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

# Get horse data from kbis.or.jp
URL = "https://www.jbis.or.jp/horse/"
MAX_INDEX = 9999999999
NULL_HORSE = "＿＿＿＿＿＿＿＿＿"

h_list = []
h_info = ['jbisコード', '馬名', '登録', '品種', '性別', '生年月日', '馬主', '毛色', '調教師', '生産牧場', '産地', '戦績', '総賞金', '市場取引', '-', '-']

# counter
ind = 0
f_incr = 0

#for _ in np.arange(1, MAX_INDEX, 1):
for _ in range(700000, MAX_INDEX):
    num = str(_)
    num = num.zfill(10)
    h_url = URL + num + '/'
    driver.get(h_url)

    h_name = None
    try:
        h_name = driver.find_element_by_class_name('hdg-l1-02').text
    except:
        pass

    if (h_name == NULL_HORSE) | (h_name == None):
        #print(h_url + ': no information listed on this page.')
        continue

    # Retrieve descriptions    
    h_desc = [num, h_name]

    # Horse'name
    print(h_url + ':' + h_name)

    # Get information table
    tb_class = driver.find_element_by_xpath('//table[@class="tbl-data-05 reset-mb-40"]')
    h_desc = h_desc + [e.text for e in tb_class.find_elements_by_xpath(".//td")]
    #print(h_desc)
    h_list.append(h_desc)

    if len(h_list) == 100:  
        f_name = 'jbis_or_jp_horse_%d.csv' % f_incr
        pd.DataFrame(h_list, columns=h_info).to_csv(out_dir + f_name, index=False, encoding='utf-8')
        print('Created %s' % f_name)

        # Emptying h_list
        h_list.clear()

        # Incrementing file name
        f_incr = f_incr + 1

# When for loop is done, create CSV one last time
f_name = 'jbis_or_jp_horse_tmp_%d.csv' % f_incr
pd.DataFrame(h_list, columns=h_info).to_csv(out_dir + f_name, index=False, encoding='utf-8')
print('Finished. Created %s' % f_name)



#driver.get()
#print(driver.page_source)
driver.quit()


# web scraping using beautifulsoup
#URL = 'https://db.netkeiba.com/'
#page = requests.get(URL)
#soup = BeautifulSoup(page.content, 'html.parser')
#result = soup.find(id='db_top')
#print(result)