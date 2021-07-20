from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from pytesseract import image_to_string
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract
import time
import os, sys
import traceback

def get_captcha_text(location, size, correct=False, file_name='screenshot.png'):
    # pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
    im = Image.open(file_name)
    print('location and size', location, size)
    left = location['x']
    top = 385
    if correct:
        top = location['y']
    right = location['x'] + size['width']
    bottom = top + size['height']
    print('left', left, 'top', top, 'right', right, 'bottom', bottom)
    im = im.crop((left, top, right, bottom))  # defines crop points    im.save('screenshot.png')
    captcha_text = image_to_string(im)
    im.save('captcha_'+file_name)
    return captcha_text

class StartProcess:

    def __init__(self, driver, dc):
        self.driver = driver
        self.dc = dc

    def start_form(self):
        self.driver.find_element_by_id('proceedcheck_english').click()
        time.sleep(2)
        self.driver.execute_script("javascript:checkProceed('ownsite')")
        self.driver.find_element_by_xpath('//*[@id="frmFeeParams"]/div/div/div[2]/div/div[2]/div').click()
        self.driver.find_element_by_xpath('//*[@id="frmFeeParams"]/div/div/div[2]/div/div[2]/div/div/ul/li[2]').click()
        time.sleep(1)

    def FillForm(self):
        name = self.driver.find_element_by_id('outref11')
        name.clear()
        name.send_keys(self.dc['name'])
        phone = self.driver.find_element_by_id('outref12')
        phone.clear()
        phone.send_keys(self.dc['phone'])
        phone = self.driver.find_element_by_id('mobileNo')
        phone.clear()
        phone.send_keys(self.dc['phone'])
        amount = self.driver.find_element_by_id('outref13')
        amount.clear()
        amount.send_keys(self.dc['amount'])
        cname = self.driver.find_element_by_id('cusName')
        cname.clear()
        cname.send_keys(self.dc['name'])
        cname = self.driver.find_element_by_id('emailId')
        cname.clear()
        cname.send_keys(self.dc['email'])
        element = self.driver.find_element_by_xpath('//*[@id="captchaImage"]')
        location = element.location
        size = element.size
        file_name = 'screenshot.png'
        self.driver.save_screenshot(file_name)
        captcha = self.driver.find_element_by_id('captchaValue')
        captcha.clear()
        captcha_text = get_captcha_text(location, size)
        print('captcha_text', captcha_text)
        captcha.send_keys(captcha_text)
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="frmFeeParams"]/div[2]/div/div[3]/div[2]/div/div[2]/img'))).click()

        selectMonth = self.driver.find_element_by_xpath(
            '//*[@id="ui-datepicker-div"]/div/div/select[1][@class="ui-datepicker-month"]')
        for option in selectMonth.find_elements_by_tag_name('option'):
            if option.text == 'Mar':
                option.click()
                break

        selectYear = self.driver.find_element_by_xpath(
            '//*[@id="ui-datepicker-div"]/div/div/select[2][@class="ui-datepicker-year"]')
        for option in selectYear.find_elements_by_tag_name('option'):
            if option.text == '2017':
                option.click()
                break

        days = self.driver.find_elements_by_class_name('ui-state-default')
        days[0].click()
        self.driver.execute_script("javascript:validateAndSubmitFeeParams('frmFeeParams')")
        print('script executed')

    def CardForm(self):
        elem = self.driver.find_element_by_id('cardNumber')
        elem.send_keys(self.dc['card'])
        elem = self.driver.find_element_by_id('expMnthSelect')
        elem.send_keys('%.2d' % self.dc['date'].month)
        elem = self.driver.find_element_by_id('expYearSelect')
        elem.send_keys(self.dc['date'].year)
        elem = self.driver.find_element_by_id('cardholderName')
        elem.send_keys(self.dc['name'])
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'cvd2')))
        elem = self.driver.find_element_by_id('cvd2')
        elem.send_keys(self.dc['cvv'])
        self.driver.execute_script("document.body.style.zoom='200%'")
        self.driver.execute_script("window.scrollTo(0, 500)")
        element = self.driver.find_element_by_xpath('//*[@id="captcha_image"]')
        location = element.location
        size = element.size
        file_name = 'screenshot1.png'
        self.driver.save_screenshot(file_name)
        # left = location['x']
        # top = location['y']
        # right = location['x'] + size['width']
        # bottom = top + size['height']
        left = 283
        top = 480
        right = 427
        bottom = 529
        im = Image.open(file_name)
        im = im.crop((left, top, right, bottom))
        im.save('captcha_' + file_name)
        self.driver.execute_script('''window.open("https://www.newocr.com/", "_blank");''')
        self.driver.switch_to.window(self.driver.window_handles[1])
        print('current_url is', self.driver.current_url)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'userfile')))
        self.driver.find_element_by_id('userfile').send_keys(os.getcwd()+'/captcha_'+file_name)
        self.driver.find_element_by_id('preview').click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'ocr')))
        self.driver.find_element_by_id('ocr').click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'ocr-result')))
        elem = self.driver.find_element_by_id('ocr-result')
        captcha_text = elem.text.strip().replace(" ", "")
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        print('after close current url', self.driver.current_url, 'captcha_text', captcha_text)
        captcha = self.driver.find_element_by_id('passline')
        # WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'text-image')))
        captcha.clear()
        captcha.send_keys(captcha_text)
        self.driver.execute_script("document.body.style.zoom='100%'")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'proceed_button')))
        self.driver.find_element_by_id('proceed_button').click()


    def OtpForm(self):
        WebDriverWait(self.driver, 10).until(EC.url_to_be('https://prdrupayias.insolutionsglobal.com/NPCI_IAS_NSDL/authOTP.do'))
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'txtipin')))
        elem = self.driver.find_element_by_id('txtipin')
        elem.send_keys(self.dc['ipin'])
        self.driver.find_element_by_id('btnverify').click()

    def Completed(self):
        self.start_form()
        exp = True
        while exp:
            try:
                self.FillForm()
                WebDriverWait(self.driver, 10).until(
                    EC.url_to_be('https://www.onlinesbi.com/sbicollect/payment/confirmpayment.htm'))
                exp = False
            except Exception as e:
                traceback.print_tb(e.__traceback__)

        self.driver.execute_script('javascript:confirmPayment()')
        self.driver.execute_script("javascript:paySubmit('RUPAYCARD')")

        WebDriverWait(self.driver, 10).until(EC.url_contains('https://sbipg.sbi/PG/paymentpage.htm?PaymentID'))
        exp = True

        while exp:
            try:
                self.CardForm()
                WebDriverWait(self.driver, 10).until(EC.url_to_be('https://prdrupayias.insolutionsglobal.com/NPCI_IAS_NSDL/authOTP.do'))
                # WebDriverWait(self.driver, 5).until(EC.url_changes)
                exp = False
            except Exception as e:
                traceback.print_tb(e.__traceback__)
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])

        self.OtpForm()
        WebDriverWait(self.driver, 20).until(
            EC.url_to_be('https://www.onlinesbi.com/sbicollect/fsssuccessresponseredirect.htm'))
        time.sleep(1)
        ref_no = self.driver.find_element_by_xpath('//*[@id="collect"]/div[2]/div/div[2]/span/strong').text
        elem = self.driver.find_elements_by_class_name('alert-danger')
        if elem:
            return ref_no, False
        elem = self.driver.find_elements_by_class_name('alert-success')
        if elem:
            return ref_no, True