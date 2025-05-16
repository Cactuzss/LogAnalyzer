import asyncio
from modules import parser
import sys
from cli import Params
from api import get_packages, get_log
import fs
from modules import CachingJSON

# for testing
import time

from test_links import TEST_LINKS

test_obj ={
        "name" : "test_name2",
        "error_message": "test_error_messag2e",
        "error_explanation": "test_error_explanation2",
        "error_solution": "test_error_solution" 
    }

#define main function
async def main():
    try:
        jc = CachingJSON()
        jc.put_in_cash_obj(test_obj)
        cashe_data = jc.get_obj_by_name(test_obj.get("name"))

        print(cashe_data)
    except Exception as e:
        print(f"eternal err exit with \n\n{e}\n\nexeption")
        exit(1)



if __name__ == "__main__":
    
    time_start = time.time()
    
    asyncio.run(main())
    
    time_end = time.time()
    
    print((time_end - time_start ))

    


