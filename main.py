import asyncio
from modules import parser, CachingJSON
import json
# for testing
import time

from test_links import TEST_LINKS

test_obj1 ={
        "name" : "test_name1",
        "error_message": "test_error_message",
        "error_explanation": "test_error_explanation2",
        "error_solution": "test_error_solution" 
    }
test_obj2 ={
        "name" : "test_name2",
        "error_message": "test_error_message",
        "error_explanation": "test_error_explanation2",
        "error_solution": "test_error_solution" 
    }
test_obj3 ={
        "name" : "test_name3",
        "error_message": "test_error_message",
        "error_explanation": "test_error_explanation2",
        "error_solution": "test_error_solution" 
    }

#define main function
async def main():
    try:
        jc = CachingJSON()
        jc.put_in_cash_obj(test_obj1)
        jc.put_in_cash_obj(test_obj2)
        jc.put_in_cash_obj(test_obj3)

        cashe_data = await jc.get_array_dists_by_msg("df")
        
        print(json.dumps(cashe_data, indent=4 ))
    except Exception as e:
        print(f"eternal err exit with \n\n{e}\n\nexeption")
        exit(1)



if __name__ == "__main__":
    
    time_start = time.time()
    
    asyncio.run(main())
    
    time_end = time.time()
    
    print((time_end - time_start ))

    


