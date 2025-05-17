from modules import CachingJSON
import asyncio
import pprint

test_obj1 ={
    "err" : {
        "error_message": "expretion",
        "error_explanation": "test_error_explanation1",
        "error_solution": "test_error_solution" ,
        "claster_name":"claster_name1"
        }
    }
test_obj4 ={
    "err" : {
        "error_message": "test_error_message",
        "error_explanation": "test_error_explanation1",
        "error_solution": "test_error_solution" ,
        "claster_name":"claster_name1"
        }
    }
test_obj2 ={
    "err" : {
        "error_message": "test_error_message",
        "error_explanation": "test_error_explanation2",
        "error_solution": "test_error_solution",
        "claster_name":"err_name"
    }
     
    }
test_obj3 ={
    "err": { 
        "error_message": "test_error_message",
        "error_explanation": "test_error_explanation3",
        "error_solution": "test_error_solution",
        "claster_name":"err_name"
        }
    }

def main():
    jc = CachingJSON()

    jc.putting(test_obj1)
    jc.putting(test_obj2)
    jc.putting(test_obj3)
    jc.putting(test_obj4)


    data = asyncio.run(jc.get_array_dists_by_claster_name("err_name"))

    pprint.pp(data)



if __name__ == "__main__":
    main()