import json
import click
import asyncio
import platform

# for testing
import time

import regex as re

from modules import Configuration, CachingJSON
from modules.api import get_failed_builds
from test_links import TEST_LINKS

# Где вызывается main()?
# В функции после декораторов @click

async def main():

    failed_builds = get_failed_builds(Configuration.branch, Configuration.architecture.value)
    print(len(failed_builds))

    test_obj1 ={
        "name" : "test_name1",
        "error_message": "test_error_message",
        "error_explanation": "test_error_explanation2",
        "error_solution": "test_error_solution" 
    }
    test_obj2 ={
        "name" : "test_name2",
        "error_message": "test_error_message",
        "error_explanation": "test_error_explanation2",
        "error_solution": "test_error_solution" 
    }
    test_obj3 ={
        "name" : "test_name3",
        "error_message": "test_error_message",
        "error_explanation": "test_error_explanation2",
        "error_solution": "test_error_solution" 
    }


    try:
        jc = CachingJSON()
        jc.put_in_cash_obj(test_obj1)
        jc.put_in_cash_obj(test_obj2)
        jc.put_in_cash_obj(test_obj3)

        cashe_data = await jc.get_array_dists_by_msg("df")
        
        print(json.dumps(cashe_data, indent=4 ))
    except Exception as e:
        print(f"eternal err exit with \n\n{e}\n\nexeption")
        exit(1)


# Startup and configuration stuff
def is_x86_64() -> bool:
    return platform.machine().endswith('64')

def is_endpoint_valid(address: str) -> bool:
    return re.match(pattern=r"^(?:\d{1,3}(?:\.|\:)){4}\d+$", string=address) is not None

@click.command()
@click.option("--arch", "-a",
              default=Configuration.AvailableArchitectures.x86_64 if is_x86_64() else Configuration.AvailableArchitectures.i586, 
              type=click.Choice(Configuration.AvailableArchitectures),
              help=f"Sets branch architecture. Available options are: 'x86_64' and 'i586'")
@click.option("--branch", "-b", default=Configuration.branch, help="Sets beehive branch")
@click.option("--model_type", "-m", default=Configuration.ModelTypes.local, 
              type=click.Choice(Configuration.ModelTypes),
              help=f"Sets model type to use. Available options are: {Configuration.ModelTypes.local} and {Configuration.ModelTypes.remote}")
@click.option("--ollama_address", "-r", default="",
              help="Required if model type is remote. Sets ollama api endpoint")
@click.option("--verbose", "-v", is_flag=True, 
              help="Set to true to more logs")
@click.option("--output", "-o", type=click.Path(writable=True, dir_okay=False), default="./log-analyzer-out.txt",
              help="Output file")
def startup(arch, branch, model_type, ollama_address, verbose, output):
    Configuration.architecture = arch
    Configuration.branch = branch
    Configuration.model_type = model_type
    Configuration.verbose = verbose

    # TODO: May be required
    if (len(output) != 0):
        Configuration.output_path = output
    
    if (Configuration.model_type == Configuration.ModelTypes.remote):
        if (is_endpoint_valid(ollama_address)):
            Configuration.remote_address = ollama_address
        else:
            # TODO: make it cool and fancy
            print(f"[ERROR]: Specified ollama address ({ollama_address}) doesn't seem like an endpoint")
            exit(1)

    
    time_start = time.time()
    
    asyncio.run(main())
    
    time_end = time.time()
    
    print((time_end - time_start ))



if __name__ == '__main__':
    startup()
