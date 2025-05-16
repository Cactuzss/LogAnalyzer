import requests
import asyncio
import regex
import sys
import time

regex_for_url = r'(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?)|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})?'


class parser:
    def get_log_by_link(link: str) -> str:
        """ open gogle chrome client
        wait 10 sec for bypass anti-bot and loadding el
        return all log in string format
        """
        try:
            if(len(link) <= 0):
                raise Exception("[ERROR_VALID] : string is empty")
            if(not regex.match(regex_for_url, link)):
                raise Exception("[ERROR_VALID] : Is not link")
            res = requests.get(link)

            if(res.status_code != 200):
                raise Exception(f"[ERROR_OPEN_PAGE] : error {res.status_code}")

            return res
    
    
        except Exception as ex:
            return "ERR "
    def get_log_by_links_array( links: list[str] ) ->str:
        """ sending get request by urls
        """
        try:
            if (type(links) is not list):
                raise Exception(f"[ERROR_VALID] : problematic data format, waitting list[str]")
            res = []
            for link in links:
                res.append(parser.get_log_by_link(link).text)
            # return res
            return "succses"
        except Exception as e:
            print(f'error in { links }\n\n[ERROR]::{e}')
            return [""]

