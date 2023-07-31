from playwright.sync_api import sync_playwright

#import bs4 
import time

mail_url = 'https://passport.yandex.ru/auth'


def get_urls():
    with sync_playwright() as p:
        login = 'cher.ne@yandex.ru'
        psw = 'xthyztdf75'
        browser = p.chromium.launch(headless= False)
        page = browser.new_page()
        page.goto(mail_url)
        page.wait_for_timeout(2000)
        page.click('text = Почта')
        page.query_selector('[name = "login"]').fill(login)
        page.click('id=passp:sign-in')
        page.wait_for_timeout(1000)
        page.query_selector('[name="passwd"]').fill(psw)
        page.click('id=passp:sign-in')
        page.wait_for_timeout(1000)
        page.goto('https://mail.yandex.ru/?uid=752034275#inbox')
        list_of_msgs = [for i in page.query_selector_all()]
        
        browser.new_page()
        time.sleep(300)
    
    
# <button data-t="button:default" 
# data-type="login"
# type="button"
# class="Button2 Button2_checked Button2_size_l Button2_view_default"
#  aria-pressed="true"
#  autocomplete="off">
#  <span class="Button2-Text">Почта</span></button>
get_urls()