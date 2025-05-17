import regex, asyncio
from modules import CachingJSON, LabelClassifier


jc = CachingJSON()
regex_for_url = r'(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?)|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})?'

def collect_data(data:list[dict], cluster_id:int,  classifier:LabelClassifier):
    
    try:
        #if not isinstance(classifier, LabelClassifier):
            #raise Exception(f"[ERROR] : non valid classifier, waitting LabelClassifier")
        #if not isinstance(data, type(list[dict])):
            #raise Exception(f"[ERROR] : non valid data, waitting list[dict] ({type(data)})")

        #if not isinstance(cluster_id, int):            
            #raise Exception(f"[ERROR] : non valid cluster_id, waitting int ({type(cluster_id)})")



        #for link in data:
            #if regex.match(regex_for_url, link.get("url")):
                #raise Exception("[ERROR] : must be url")

        
        # temp_obj = {
        #     "cluster_id":cluster_id,
        #     "data":[

        #     ]
        # }

        # for i in range(0, len(links)):
        #     temp_obj.get("data").append({link[i]: data[i]})


        # asyncio.run(jc.putting('temp', "claster", temp_obj))

        # request to lrm
        generate_data = classifier.generate_log_description(data, cluster_id)
        """
        {
        
        "cluster_name":err_type,
        err_exp:,
        err_sol:
        }
        """


        result_data = {
            "cluster_id":cluster_id,
            "generate_data":generate_data,
            "data":[]
        }

        for i in range(0, len(data)):
            result_data.get("data").append({
                "link":data[i].get("url"),
                "log_text":data[i].get("data")
            })
        """
        {
            "cluster_id":cluster_id
            "generatedata":{
                "cluster_name":type,
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

