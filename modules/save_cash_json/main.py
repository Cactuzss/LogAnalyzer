from jsoncache import JSONCache


class CachingJSON:
    def __init__(self, parameters = {}):
        self.jc = JSONCache(autosave=False)
    async def put_array(self, branch: str,key:str , values:list[dict])->None:
        try:
            if not isinstance(branch, str) and not isinstance(key, str):
                raise Exception(f'[ERR_VALID] : can\' read property "branch, key" with type {type(branch)}/{type(key)}, please enter str')
            for i in values:
                await self.putting(branch,key, i)
        except Exception as e:
            print(f"[CACHE_ERROR] : {e}")

    async def putting(self,branch,key, obj:any):
        try:
            inpt_data = {
                key:obj
            }

            # validation 
            try:
                d = self.jc.get(branch)
                d.append(inpt_data)
                self.jc.put(branch, d)
            except:
                self.jc.put(branch,[inpt_data] )
        
        except Exception as e:
            print(f"[CACHE_ERROR] : {e}")

    async def get_all_cashe_data(self, branch):
        try:
            if not isinstance(branch, str):
                raise Exception(f'[ERR_VALID] : can\' read property "branch" with type {type(branch)}, please enter str')
            try:
                return self.jc.get(branch)

            except:
                return []
        except Exception as e:
            print(f"[CACHE_ERROR] : {e}")

    async def get_array_data(self,branch:str, key:str, property:str,  value:str=""):
        try:
            if not isinstance(branch, str) and not isinstance(key, str) and not isinstance(value, str) and not isinstance(property, str):
                raise Exception(f'[ERR_VALID] : can\' read property "branch, key, property, value" with type, please enter str')
            data = self.jc.get(branch)
            result = []
        
            for d in data:
                if d.get(key).get(property) == value or value == "":
                    result.append(d.get(key, property))
        except Exception as e:
            print(f"[CACHE_ERROR] : {e}")
        return result
    
    
