from jsoncache import JSONCache


class CachingJSON:
    def __init__(self, parameters = {}):
        self.jc = JSONCache(autosave=False)
    async def put_array_dicts(self, dicts:list[dict])->None:
        try:
            if not isinstance(dicts, list[dict]):
                raise Exception('[ERR_VALID] : don\'t correct format, input list[dist]')
            for i in dicts:
                self.putting(i)
        except Exception as e:
            print(f"[CACHE_ERROR] : {e}")

    async def putting(self, obj:dict):
        try:
            if not isinstance(obj, dict):
                raise Exception('[ERR_VALID] : don\'t correct format, input dist')
            try:
                d = self.jc.get('main')
                d.append(obj)
                self.jc.put('main', d)
            except:
                self.jc.put('main',[obj] )
        
        except Exception as e:
            print(f"[CACHE_ERROR] : {e}")

    async def get_all_cashe_data(self):
        try:
            return self.jc.get('main')
            
        except:
            return []

    async def get_array_dists_by_err_msg(self, error_message:str):
        try:
            if not isinstance(error_message, str):
                raise Exception('[ERR_VALID] : don\'t correct format, input str')
            data = self.jc.get('main')
            result = []
        
            for d in data:
                if d.get('err').get('error_message') == error_message:
                    result.append(d.get('err'))
        except Exception as e:
            print(f"[CACHE_ERROR] : {e}")
        return result
    
    async def get_array_dists_by_claster_name(self, claster_name:str):
        try:
            if not isinstance(claster_name, str):
                raise Exception('[ERR_VALID] : don\'t correct format, input str')
            data = self.jc.get('main')
            result = []
        
            for d in data:
                if d.get('err').get('claster_name') == claster_name:
                    result.append(d.get('err'))
        except Exception as e:
            print(f"[CACHE_ERROR] : {e}")
        return result
