from playwright.sync_api import sync_playwright
from config import login, psw
from datetime import datetime

mail_url = 'https://passport.yandex.ru/auth'
folder_url = 'https://mail.yandex.ru/?uid=752034275#folder/22'




def get_data():
    months = {'января': 1, #dictionary for convert data to datetime
                  'февраля': 2,
                  'марта': 3,
                  'апреля': 4,
                  'мая': 5,
                  'июня': 6,
                  'июля': 7,
                  'августа': 8,
                  'сентября': 9,
                  'октября': 10,
                  'ноября': 11,
                  'декабря': 12
                  }
    url_list = []#list of urls with time

    year = datetime.now().year#number of current year for converting

    with sync_playwright() as p:
        #login
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
            url =page.query_selector('a[class = "46809b2d9d518540button-link"]').get_attribute('href')

            #time as list (need to convert to time format)

            data = page.query_selector('div[class = "6943960f0ad08528event-info"]').text_content().split()
            
            #convert list into datetime
            month = months[data[1]]
            day = data[0]
            t = data[2]
            data = datetime.strptime(f"{year}/{month}/{day} {t}","%Y/%m/%d %H:%M")
            
            url_list.append([url,data])

            page.go_back()

        return url_list