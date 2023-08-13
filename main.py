import OBS
import mail_parser
import asyncio
import db
from datetime import datetime


is_planned = 0
is_recording = 0
plan = []
    

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
    if(is_planned):#if we have planned lecture

        if(is_recording):#if we record lecture

            if (mail_parser.check_the_end(plan[0])):#if its the end of lecture
                pass
                #stop recording
                #close app 
                #delete record from database
                #get new record if its
                
        elif(is_time(plan[1])):
            pass
            #run recording
            #is_recording = 1
        else:
            pass
            #sleep(300)

            
        
    else:#get planned lecture
        record = db.get_last_record()
        if(record is not None):
            plan.append(record[0],record[1])


async def main():
    await asyncio.gather(parsing_stream(),recording_stream())

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
