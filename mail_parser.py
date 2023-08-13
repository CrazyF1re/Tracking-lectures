from playwright.async_api import async_playwright
from config import login, psw
from datetime import datetime




mail_url = 'https://passport.yandex.ru/auth'
folder_url = 'https://mail.yandex.ru/?uid=752034275#folder/22'

async def get_data():
    
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

    async with async_playwright() as p:
        #login
        browser =await p.chromium.launch(headless= False)
        page =await browser.new_page()
        await page.goto(mail_url)
        await page.wait_for_url(mail_url)
        await page.click('text = Почта')
        await (await page.query_selector('[name = "login"]')).fill(login)
        await page.click('id=passp:sign-in')
        await page.wait_for_timeout(500)
        await (await page.query_selector('[name="passwd"]')).fill(psw)
        await page.click('id=passp:sign-in')
        await page.wait_for_timeout(1000)
        await page.goto(folder_url)
        await page.wait_for_timeout(1500)
        

        #load all messages for today
        messages =await  page.query_selector_all('span[class = mail-MessageSnippet-Item_dateText]')
        while (await messages.pop().text_content()).find(':') != -1:
            await (await page.query_selector('[class= _nb-button-content]')).click()
            messages = await page.query_selector_all('[class = mail-MessageSnippet-Item_dateText]')

        #find index of first message today
        for i in messages:
            if  (await i.text_content()).find(':') == -1 :
                index = messages.index(i)
                break
        index+=2
        #if noone msg sent today    
        if index == 0:
            return
        
        #get time and urls
        pages  =await  page.query_selector_all('a[class = "mail-MessageSnippet js-message-snippet toggles-svgicon-on-important toggles-svgicon-on-unread"]')
        for i in range(index): 
            await pages[i].click()
            await page.wait_for_timeout(1000)
            #url
            url = await (await page.query_selector('a[class = "46809b2d9d518540button-link"]')).get_attribute('href')

            #time as list (need to convert to time format)

            data = str(await (await page.query_selector('div[class = "6943960f0ad08528event-info"]')).text_content()).split()
            
            #convert list into datetime
            month = months[data[1]]
            day = data[0]
            t = data[2]
            data = datetime.strptime(f"{year}/{month}/{day} {t}","%Y/%m/%d %H:%M")
            
            url_list.append([url,data])

            await page.go_back()

        return url_list
    
