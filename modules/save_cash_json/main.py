from jsoncache import JSONCache


class CachingJSON:
    def __init__(self, parameters = {}):
        self.jc = JSONCache()

    def put_in_cash_obj(self, jsonobj: dict[str, str] = {}):
        """
        parametr values:
        name : "name",
        error_message: "error_message",
        error_explanation: "error_explanation",
        error_solution: "error_solution" 
        """

        try:
            self.jc.put(jsonobj.get("name"),"error_message", jsonobj.get("error_message") )
            self.jc.put(jsonobj.get("name"),"error_explanation", jsonobj.get("error_explanation"))
            self.jc.put(jsonobj.get("name"),"error_solution", jsonobj.get("error_solution"))


        except Exception as e:
            print(f"error \n{e}")

    def get_obj_by_name(self, name:str = ""):
        try:
            return self.jc.get(name)
            
        except Exception as e:
            print(f"error {e}")
