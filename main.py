from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException as UAPE
from util import *
import csv
import sys
from datetime import datetime, date
import os
import traceback

BASE_DIR = os.getcwd()
url = 'https://www.onlinesbi.com/sbicollect/icollecthome.htm?corpID=3840368'

try:
    f = open("file.csv")
    data = csv.reader(f)
except Exception as e:
    print('file not found')
    sys.exit()

print(BASE_DIR)

driver = webdriver.Chrome(str(BASE_DIR) + '\chromedriver.exe')
# driver = webdriver.Chrome(str(BASE_DIR) + '/chromedriver')
driver.set_window_size(1050, 721)

rows = []

last = date(2022, 8, 31)

if date.today() < last:
    for i in data:
        dc = {}
        dc['card'] = i[0]
        dc['date'] = datetime.strptime(i[1], '%m/%Y')
        dc['cvv'] = i[2]
        dc['ipin'] = i[3]
        dc['rname'] = i[4]
        dc['name'] = i[5]
        dc['email'] = i[6]
        dc['phone'] = i[7]
        dc['amount'] = i[8]
        driver.get(url)
        sp = StartProcess(driver, dc)
        try:
            ref_no, resp = sp.Completed()
            i.extend([ref_no, resp])
            rows.append(i)
        except Exception as e:
            with open('log.txt', 'a') as f:
                f.write(str(e))
                f.write(traceback.format_exc())
            traceback.print_tb(e.__traceback__)

    print('rows', rows)

    with open('output.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        writer.writerows(rows)

driver.quit()