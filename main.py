import asyncio
from modules import parser

#define main function
def main():
    try:
        # print(parser.get_log_by_links_array(['https://git.altlinux.org/beehive/logs/Sisyphus/x86_64/latest/error/DirectXShaderCompiler-1.8.2403-alt0.3'])[0])
        print(parser.get_log_by_links_array('https://git.altlinux.org/beehive/logs/Sisyphus/x86_64/latest/error/DirectXShaderCompiler-1.8.2403-alt0.3')[0])
        print(parser.get_log_by_links_array(123)[0])
        print(parser.get_log_by_links_array([123, "dfdsgf"])[0])
    except Exception as e:
        print(f"eternal err exit with \n\n{e}\n\nexeption")
        exit(1)

if __name__ == "__main__":
    main()