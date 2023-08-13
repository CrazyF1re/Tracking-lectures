import OBS
import mail_parser
import asyncio
import db

is_planned = 0

async def parsing_stream():
    lst = await mail_parser.get_data()

    await db.set_data(lst)
    
    await asyncio.sleep(3600) 

async def recording_stream():
    if(not is_planned):
        #plan and change flag
        pass


async def main():
    await asyncio.gather(parsing_stream(),recording_stream())

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
