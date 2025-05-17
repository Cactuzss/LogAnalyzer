import requests
import asyncio
import regex
import sys
import time
import aiohttp
import re

regex_for_url = r'(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?)|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})?'


class parser:
    @staticmethod
    async def get_log_by_link(link: str, session: aiohttp.ClientSession) -> str:
        """ 
        """
        try:
            if(len(link) <= 0):
                raise Exception("[ERROR_VALID] : string is empty")
            if(not regex.match(regex_for_url, link)):
                raise Exception("[ERROR_VALID] : Is not link")
            
            async with session.get(link) as response:
                if response.status != 200:
                    raise Exception(f"[ERROR_OPEN_PAGE] : error {response.status}")
                
                result = {
                    "url": link,
                    "data": (await response.text()).replace("'", '').replace('"', ''),
                    "date" : response.headers.get("date")
                }


                return result
    
        except Exception as ex:
            print(f"Error processing {link}: {str(ex)}")
            return None

    @staticmethod
    async def get_log_by_links_array(links: list[str]) -> list[dict[str,str,str]]:
        """ sending get request by urls asynchronously
        """
        try:
            if not isinstance(links, list):
                raise Exception("[ERROR_VALID] : problematic data format, waiting list[str]")
            
            async with aiohttp.ClientSession() as session:
                tasks = []
                for link in links:
                    task = asyncio.create_task(parser.get_log_by_link(link, session))
                    tasks.append(task)
                    
                results = await asyncio.gather(*tasks)
                print(f"Processed {len(results)} links")
                return results
        
        except Exception as e:
            print(f'Error in processing links array:\n[ERROR]::{e}')
            return None

    @staticmethod
    def get_log_by_links_array_sync(links: list[str]) -> list[str]:
        
        if not isinstance(links, list):
            raise Exception("[ERROR_VALID] : problematic data format, waiting list[str]")
        """Synchronous wrapper for the asynchronous function"""
        return asyncio.run(parser.get_log_by_links_array(links))

