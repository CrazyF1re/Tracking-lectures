from playwright.async_api import async_playwright
from datetime import datetime
import json

#mail_url = 'https://mail.yandex.ru/?uid=752034275#inbox'
folder_url = 'https://mail.yandex.ru/?uid=752034275#folder/22'

async def click_captcha(page):
    try:
        await (await  page.query_selector('input[id=js-button]')).click()
        await page.wait_for_timeout(5000)
        await page.goto(folder_url)
        await page.wait_for_timeout(2000)

    except:
        pass

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

    async with async_playwright() as p:
        browser =await p.chromium.launch(headless= True)
        page =await browser.new_page()

        with open('cookies.json','r') as f:
            await page.context.add_cookies(json.loads(f.read()))

        await page.goto(folder_url)
        await click_captcha(page)
        
        #get time and urls        
        pages  =await  page.query_selector_all('span[class= mail-MessageSnippet-FromText]')
        times = await page.query_selector_all('span[class= mail-MessageSnippet-Item_dateText]')
        for i in range(len(pages)): 

            if await pages[i].text_content() != 'Webinar' or '.' in await times[i].text_content():
                continue

            await pages[i].click()
            await page.wait_for_timeout(1200)

            url = await (await page.query_selector('a[class = "46809b2d9d518540button-link"]')).get_attribute('href')
            data = str(await (await page.query_selector('div[class = "6943960f0ad08528event-info"]')).text_content()).split()
            
            #convert list into timestamp
            data = datetime.strptime(f"{datetime.now().year}/{months[data[1]]}/{data[0]} {data[2]}","%Y/%m/%d %H:%M").timestamp()+3600*4
            
            if datetime.now().timestamp()< data:
                url_list.append([url,data])    

            await page.go_back()
        await page.close()
        await browser.close()
        return url_list
    
async def check_the_end(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless = True)
        page = await browser.new_page()
        await page.goto(url)
        try:
            await page.query_selector('h2[text= Завершено]')
            await page.close()
            await browser.close()
            return 1
        except:
            await page.close()
            await browser.close()
            return 0
        
        