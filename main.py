import asyncio
from modules import parser
import sys
from cli import Params
from api import get_packages, get_log
import fs

# for testing
import time

import test_links

#define main function
async def main():
    try:
        
        parsed_links = await parser.get_log_by_links_array(test_links)
        print(len(parsed_links))

        i = 0
        for link in parsed_links:
            if(link != ""):
                i+=1       
        print(i)
    except Exception as e:
        print(f"eternal err exit with \n\n{e}\n\nexeption")
        exit(1)



if __name__ == "__main__":
    
    time_start = time.time()
    
    asyncio.run(main())
    
    time_end = time.time()
    
    print((time_end - time_start ))

    


