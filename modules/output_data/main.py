import regex, asyncio
from modules import CachingJSON, LabelClassifier
from modules import Preprocessor


jc = CachingJSON()
regex_for_url = r'(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?)|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})?'

def collect_data(data:list[dict], cluster_id:int,  classifier:LabelClassifier):
    strdata = ""
    data = data[:min(4, len(data))]

    for el in data:
        strdata += el["data"] + "\n"

    preprocessed = Preprocessor.process_log(strdata)
    snippets = "\n".join([p["error_snippet"] for p in preprocessed])

    generate_data = classifier.generate_log_description(snippets, cluster_id)
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





