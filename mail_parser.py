from playwright.sync_api import sync_playwright
from config import login, psw

import time

mail_url = 'https://passport.yandex.ru/auth'
folder_url = 'https://mail.yandex.ru/?uid=752034275#folder/22'
message_url = 'https://mail.yandex.ru/?uid=752034275#message/'

def get_data():
    with sync_playwright() as p:

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
        page.wait_for_timeout(1500)
        page.goto(folder_url)
        page.wait_for_url(folder_url)
        page.wait_for_timeout(1000)

        #load all messages for today
        messages = page.query_selector_all('[class = mail-MessageSnippet-Item_dateText]')
        while messages.pop().text_content().find(':') != -1:
            page.query_selector('[class= _nb-button-content]').click()
            messages = page.query_selector_all('[class = mail-MessageSnippet-Item_dateText]')

        #find index of first message today
        for i in messages:
            if  i.text_content().find(':') == -1 :
                index = messages.index(i)
                break

        #if noone msg sent today    
        if index == 0:
            return
        
        #get time and urls
        pages  = page.query_selector_all('a[class = "mail-MessageSnippet js-message-snippet toggles-svgicon-on-important toggles-svgicon-on-unread"]')
        for i in range(index): 
            pages[i].click()
            page.wait_for_timeout(1000)
            #url
            print(page.query_selector('a[class = "46809b2d9d518540button-link"]').get_attribute('href'))

            #time as list (need to convert to time format)
            print(page.query_selector('div[class = "6943960f0ad08528event-info"]').text_content().split())

            page.go_back()
        time.sleep(300)
    

get_data()