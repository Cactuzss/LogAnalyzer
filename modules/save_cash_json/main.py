from jsoncache import JSONCache
import time


class CachingJSON:
    def __init__(self, parameters = {}):
        self.jc = JSONCache()
    def putting(self, *args):

        self.jc.put('main',args[0], args[1], args[2])

    def put_in_cash_obj(self, jsonobj: dict[str, str]):
        """
        parametr values:
        name : "name",
        error_message: "error_message",
        error_explanation: "error_explanation",
        error_solution: "error_solution" 
        """

        try:
            self.putting(jsonobj.get("name"),"error_message", jsonobj.get("error_message") )
            self.putting(jsonobj.get("name"),"error_explanation", jsonobj.get("error_explanation"))
            self.putting(jsonobj.get("name"),"error_solution", jsonobj.get("error_solution"))

        except Exception as e:
            print(f"error \n{e}")

    def get_obj_by_name(self, name:str = ""):
        try:
            return self.jc.get(name)
            
        except Exception as e:
            print(f"error {e}")

    async def get_array_dists_by_msg(self, error_message:str):
        data = self.jc.get("main")

        return data
