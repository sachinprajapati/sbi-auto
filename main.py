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
from datetime import datetime
import os

BASE_DIR = Path(__file__).resolve().parent
url = 'https://www.onlinesbi.com/sbicollect/icollecthome.htm?corpID=3681157'

try:
    f = open("file.csv")
    data = csv.reader(f)
except Exception as e:
    print('file not found')
    sys.exit()

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : os.getcwd()}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome('./chromedriver', options=chromeOptions)
driver.set_window_size(1050, 721)

rows = []

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
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

print('rows', rows)

with open('output.csv', 'w') as csvoutput:
    writer = csv.writer(csvoutput, lineterminator='\n')
    writer.writerows(rows)

driver.quit()