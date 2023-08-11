import OBS
import mail_parser
import asyncio

is_planned = 0

async def parsing_stream():
    lst = await mail_parser.get_data()

    #filter urls that repits (now its like a set)
    if type(lst) == list:
        with open('list.txt','r') as f:
            global_lst = f.readlines()
        
        for i in lst:
            flag = 1
            for line in global_lst:
                if i.split(' ')[0]  in line:
                    flag = 0
            if flag:
                global_lst.append(i)

        with open('list.txt','w') as f:
            f.writelines(global_lst)
    await asyncio.sleep(3600) 

async def recording_stream():
    if(not is_planned):
        #plan and change flag
        pass


async def main():
    await asyncio.gather(parsing_stream(),recording_stream())

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
