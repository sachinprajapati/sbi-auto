from pathlib import Path
import asyncio
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

BASE_DIR = Path(__file__).resolve().parent
url = 'https://www.onlinesbi.com/sbicollect/icollecthome.htm?corpID=3681157'

try:
    f = open("file.csv")
    data = csv.reader(f)
except Exception as e:
    print('file not found')
    sys.exit()


driver = webdriver.Chrome(str(BASE_DIR) + '/chromedriver.exe')
# driver = webdriver.Chrome(str(BASE_DIR) + '/chromedriver')
driver.set_window_size(1050, 721)

rows = []

last = date(2021, 8, 5)

if date.today() < last:
    for i in data:
        dc = {}
        dc['card'] = i[0]
        dc['date'] = datetime.strptime(i[1], '%m/%Y')
        dc['cvv'] = i[2]
        dc['ipin'] = i[3]
        dc['name'] = i[4]
        dc['email'] = i[5]
        dc['phone'] = i[6]
        dc['amount'] = i[7]
        driver.get(url)
        sp = StartProcess(driver, dc)
        try:
            ref_no, resp = sp.Completed()
            i.extend([ref_no, resp])
            rows.append(i)
        except Exception as e:
            traceback.print_tb(e.__traceback__)

    print('rows', rows)

    with open('output.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        writer.writerows(rows)

driver.quit()