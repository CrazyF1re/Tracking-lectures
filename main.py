import db
from OBS import OBS
import mail_parser
import asyncio
from datetime import datetime
import time

is_planned = 0
is_recording = 0
plan = []
obs = OBS() 
async def is_time(time):
    if (time - datetime.now().timestamp() < 300):
        return 1
    return 0


async def parsing_stream():
    lst = await mail_parser.get_data()
    if lst is not None:
        await db.set_data(lst)
    await asyncio.sleep(3600) 

async def recording_stream():
    await asyncio.sleep(300) 
    global is_planned
    if(is_planned):#if we have planned lecture

        if(is_recording):#if we record lecture

            if (mail_parser.check_the_end(plan[0])):#if its the end of lecture
                obs.stop_recording()
                obs.close_app()
                db.delete_url(plan[0])
                plan.pop()
                is_planned = 0
                is_recording = 0
                
        elif(is_time(plan[1])):
            obs.run()
            obs.set_up_sourse()
            obs.set_url(plan[0])
            obs.start_recording()
            is_recording = 1
            
    else:#get planned lecture
        record = await db.get_last_record()
        if(record is not None):
            plan.append(record[0])
            plan.append(record[1])
            is_planned = 1


async def main():
    await asyncio.gather(parsing_stream(),recording_stream())

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
