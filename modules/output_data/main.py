import regex, asyncio
from modules import CachingJSON, LabelClassifier


jc = CachingJSON()
regex_for_url = r'(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?)|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})?'

def collect_data(data:list[str], claster_name:str, links:list[str], classifire:LabelClassifier):
    """
    dictionary format:
    {
        "claster_name":[{
            "link":"text_log"
        }...]

    }
    """
    try:
        if not isinstance(classifire, LabelClassifier):
            raise Exception(f"[ERROR] : non valid data, waitting LabelClassifier")
        if not isinstance(data, type(list[str])):
            raise Exception(f"[ERROR] : non valid data, waitting list[str]")

        if not isinstance(claster_name, str):            
            raise Exception(f"[ERROR] : non valid data, waitting str")

        if not isinstance(links, list[str]):            
            raise Exception(f"[ERROR] : non valid data, waitting list[str]")


        for link in data.get("list_links"):
            if regex.match(regex_for_url, link):
                raise Exception("[ERROR] : must be link")
        if len(links) != len(data):            
            raise Exception(f"[ERROR] : len(links) must be equal len(data)")

        
        # temp_obj = {
        #     "claster_name":claster_name,
        #     "data":[

        #     ]
        # }

        # for i in range(0, len(links)):
        #     temp_obj.get("data").append({link[i]: data[i]})


        # asyncio.run(jc.putting('temp', "claster", temp_obj))

        # request to lrm
        generate_data = classifire.generate_log_description(data, claster_name)
        """
        {
        err_msg:,
        err_exp:,
        err_sol:
        }
        """


        result_data = {
            "claster_name":claster_name,
            "generate_data":generate_data,
            "data":[]
        }

        for i in range(0, len(links)):
            result_data.get("data").append({
                "link":links[i],
                "log_text":data[i]
            })
        """
        {
            "claster_name":claster_name,
            "generatedata":{
                "msg":msg,
                "exp":exp,
                "solve":solve
            }
            data:[{
                    "link":link
                    "log_text":log_text
                }...
            ]
        }
        """
        return result_data




    except Exception as e:
        print(e)

