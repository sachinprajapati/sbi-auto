from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from pytesseract import image_to_string
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract
import time
import os, sys
import traceback
import random, string

def get_captcha_text(location, size, correct=False, file_name='screenshot.png'):
    im = Image.open(file_name)
    left = 460
    top = 327
    right = 600
    bottom = 360
    im = im.crop((left, top, right, bottom))  # defines crop points    im.save('screenshot.png')
    captcha_text = image_to_string(im)
    im.save('captcha_'+file_name)
    return captcha_text

def get_second_text(file_name='screenshot1.png'):
    im = Image.open(file_name)
    left = 650
    top = 438
    right = 800
    bottom = 500
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
        WebDriverWait(self.driver, 10).until(EC.url_to_be('https://www.onlinesbi.sbi/sbicollect/sbclink/displayinstitutiontype.htm'))
        elem = self.driver.find_element_by_css_selector('[data-id="selStateName"]')
        elem.click()
        time.sleep(1)
        elem = self.driver.find_element_by_xpath('//*[@id="stateID"]/div/div/ul/li[36]/a/span[1]')
        elem.click()
        time.sleep(1)
        # elem = self.driver.find_element_by_css_selector('[data-id="instTypeID"]')
        # elem.click()
        elem = self.driver.find_element_by_id('instTypeID')
        elem.send_keys('Educational Institutions')
        # time.sleep(1)
        # elem.select_by_value('IN00058245')
        self.driver.execute_script('javascript:submitSelectedStateAndType()')
        WebDriverWait(self.driver, 10).until(EC.url_to_be('https://www.onlinesbi.sbi/sbicollect/payment/listinstitution.htm'))
        elem = self.driver.find_element_by_css_selector('[data-id="selectedInstID"]')
        elem.click()
        time.sleep(1)
        # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'selectedInstID')))
        # elem = self.driver.find_element_by_id('selectedInstID')
        # elem.send_keys('IN00058245')
        time.sleep(1)
        elem = self.driver.find_element_by_xpath('//*[@id="select-institute"]/div/div/ul/li[159]/a/span[1]')
        elem.click()
        self.driver.execute_script("javascript:submitInstitutionDetail('Educational Institutions')")
        WebDriverWait(self.driver, 10).until(EC.url_to_be('https://www.onlinesbi.sbi/sbicollect/payment/listcategory.htm'))
        self.driver.find_element_by_xpath('//*[@id="frmFeeParams"]/div/div/div[2]/div/div[2]/div').click()
        self.driver.find_element_by_xpath('//*[@id="frmFeeParams"]/div/div/div[2]/div/div[2]/div/div/ul/li[4]').click()
        time.sleep(1)

    def FillForm(self):
        # bill = self.driver.find_element_by_id('outref11')  #BILL NO
        # bill.clear()
        # bill.send_keys(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)))
        name = self.driver.find_element_by_id('outref12')   #NAME
        name.clear()
        name.send_keys(self.dc['amount'])
        remarks = self.driver.find_element_by_id('transactionRemarks')   #REMARKS
        remarks.clear()
        remarks.send_keys(self.dc['rname']+self.dc['card'])
        phone = self.driver.find_element_by_id('mobileNo')
        phone.clear()
        phone.send_keys(self.dc['phone'])
        # amount = self.driver.find_element_by_id('outref13')
        # amount.clear()
        # amount.send_keys(self.dc['amount'])
        cname = self.driver.find_element_by_id('cusName')
        cname.clear()
        cname.send_keys(self.dc['name'])
        cname = self.driver.find_element_by_id('emailId')
        cname.clear()
        cname.send_keys(self.dc['email'])
        # self.driver.execute_script("window.scrollTo(0, 500)")
        # element = self.driver.find_element_by_xpath('//*[@id="captchaImage"]')
        # element = self.driver.find_element_by_id('imageContainer')
        # location = element.location
        # size = element.size
        # file_name = 'screenshot.png'
        # self.driver.save_screenshot(file_name)
        # captcha = self.driver.find_element_by_id('captchaValue')
        # captcha.clear()
        # captcha_text = get_captcha_text(location, size)
        # print('captcha_text', captcha_text)
        # assert not captcha_text.isalnum()
        # captcha.send_keys(captcha_text)
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="frmFeeParams"]/div[2]/div/div[3]/div[2]/div/div[2]/img'))).click()

        days = self.driver.find_elements_by_class_name('ui-state-default')
        days[0].click()
        # self.driver.execute_script("javascript:validateAndSubmitFeeParams('frmFeeParams')")
        print('script executed')

    def CardForm(self):
        elem = self.driver.find_element_by_id('cardNumber')
        elem.send_keys(self.dc['card'])
        elem = self.driver.find_element_by_id('expMnthSelect')
        elem.click()
        time.sleep(1)
        elem.send_keys('%.2d' % self.dc['date'].month)
        elem = self.driver.find_element_by_id('expYearSelect')
        elem.send_keys(self.dc['date'].year)
        elem = self.driver.find_element_by_id('cardholderName')
        elem.send_keys(self.dc['name'])
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'cardCvv')))
        elem = self.driver.find_element_by_id('cardCvv')
        elem.send_keys(self.dc['cvv'])
        self.driver.execute_script("document.body.style.zoom='200%'")
        self.driver.execute_script("window.scrollTo(0, 500)")
        element = self.driver.find_element_by_xpath('//*[@id="captcha_image"]')
        location = element.location
        size = element.size
        file_name = 'screenshot1.png'
        self.driver.save_screenshot(file_name)
        left = 650
        top = 415
        right = 800
        bottom = 465
        im = Image.open(file_name)
        im = im.crop((left, top, right, bottom))
        im.save('captcha_' + file_name)
        captcha_text = get_second_text()
        print('after close current url', self.driver.current_url, 'captcha_text', captcha_text)
        captcha = self.driver.find_element_by_id('passline')
        # WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'text-image')))
        captcha.clear()
        captcha.send_keys(captcha_text)
        self.driver.execute_script("document.body.style.zoom='100%'")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'proceed_button')))
        self.driver.find_element_by_id('proceed_button').click()


    def OtpForm(self):
        print("in otp form")
        if len(self.dc['ipin']) == 4:
            # WebDriverWait(self.driver, 10).until(EC.url_to_be('https://prdrupayias.insolutionsglobal.com/NPCI_IAS_NSDL/authOTP.do'))
            # WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'txtipin')))
            # elem = self.driver.find_element_by_id('txtipin')
            # elem.send_keys(self.dc['ipin'])
            # self.driver.find_element_by_id('btnverify').click()
            WebDriverWait(self.driver, 10).until(EC.url_to_be('https://isg-3dsecure.in/GeniusVACS-NSDL/PaRequestHandler'))
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'pwd')))
            elem = self.driver.find_element_by_id('pwd')
            elem.send_keys(self.dc['ipin'])
            self.driver.find_element_by_id('btnSubmitId').click()
        if len(self.dc['ipin']) == 9:
            WebDriverWait(self.driver, 10).until(
                EC.url_to_be('https://acssp.thecardservicesonline.com/mdpayacs/pareq'))
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'IPIN')))
            elem = self.driver.find_element_by_id('IPIN')
            elem.send_keys(self.dc['ipin'])
            self.driver.find_element_by_id('IDCT_BUTID').click()
        else:
            WebDriverWait(self.driver, 10).until(
                EC.url_to_be('https://paysecure.yalamanchili.in/naradaacsweb/acs/authenticate'))
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'ipin')))
            elem = self.driver.find_element_by_id('ipin')
            elem.send_keys(self.dc['ipin'])
            self.driver.find_element_by_id('otpbut').click()

    def Completed(self):
        self.start_form()
        exp = True
        fcount = 1
        while exp:
            try:
                self.FillForm()
                print('after fill form')
                WebDriverWait(self.driver, 30).until(
                    EC.url_contains('sbicollect/payment/confirmpayment.htm'))
                print('after confirmpayment wait')
                self.driver.execute_script('javascript:confirmPayment()')
                self.driver.execute_script("javascript:paySubmit('PREPAID')")
                WebDriverWait(self.driver, 10).until(EC.url_contains('https://sbipg.sbi/PG/paymentpage.htm'))
                exp = False
            except Exception as e:
                print('exception', e)
                # traceback.print_tb(e.__traceback__)
                # self.driver.refresh()
                fcount += 1
                if fcount == 3:
                    print("if start form times", fcount)
                    return None, False

        # self.driver.execute_script('javascript:confirmPayment()')
        # self.driver.execute_script("javascript:paySubmit('RUPAYCARD')")
        #
        # WebDriverWait(self.driver, 10).until(EC.url_contains('https://sbipg.sbi/PG/paymentpage.htm?PaymentID'))
        exp = True
        count = 1

        while exp:
            try:
                url = self.driver.current_url
                print('url for card form', url)
                self.CardForm()
                time.sleep(2)
                if url == self.driver.current_url:
                    raise ValueError('Not submitted')
                # WebDriverWait(self.driver, 10).until(EC.url_to_be('https://prdrupayias.insolutionsglobal.com/NPCI_IAS_NSDL/authOTP.do'))
                # WebDriverWait(self.driver, 5).until(EC.url_changes)
                if not 'Invalid captcha' in self.driver.page_source:
                    exp = False
            # except AssertionError:
            #     print('except AssertionError text not recognised')
            #     if len(self.driver.window_handles) > 1:
            #         self.driver.close()
            #         self.driver.switch_to.window(self.driver.window_handles[0])
            #         print('window closed')
            #         self.driver.refresh()
            #         print('refresh page')
            except Exception as e:
                traceback.print_tb(e.__traceback__)
                print("nos of tab", len(self.driver.window_handles))
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    print('window closed')
                    self.driver.refresh()
                    print('refresh page')
                count += 1
                if count == 5:
                    print("if card form", count)
                    return None, False
        print('url for card form before otp', self.driver.current_url)
        self.OtpForm()
        WebDriverWait(self.driver, 20).until(
            EC.url_to_be('https://www.onlinesbi.com/sbicollect/fsssuccessresponseredirect.htm'))
        time.sleep(1)
        elem = self.driver.find_elements_by_class_name('alert-danger')
        if elem:
            print('alert-danger', len(elem))
            ref_no = self.driver.find_element_by_xpath('//*[@id="collect"]/div[2]/div/div[2]/span/strong').text
            return ref_no, False
        elem = self.driver.find_elements_by_class_name('alert-success')
        if elem:
            print('alert-success', len(elem))
            ref_no = self.driver.find_element_by_xpath('//*[@id="printdetailsformtop"]/div/div/div[2]/span/strong').text
            return ref_no, True