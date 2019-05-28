import argparse
import asyncio
import getpass
import sys
import webbrowser

from aiohttp import ClientConnectorError

from .dumper import Dumper
from .vk import VK

__description__ = 'Dump photos from your VK account.'

DEFAULT_OUTPUT = 'dump'

INSTRUCTIONS_TO_OBTAIN_ACCESS_TOKEN = '''
To get the access token:
1. Log in to VK in the newly opened browser tab (if not already).
2. Allow the app to access your photos.
3. After successful application authorization and redirection to the next 
page, copy the access token from the browser line.
'''.strip()

ASK_ACCESS_TOKEN = 'Access Token: '

CLIENT_CONNECTION_ERROR_TEXT = '''
Connection error occurred! Please check your network connection.
'''

IO_ERROR_TEXT = '''
IO error occurred! Please check your output path.
'''

UNKNOWN_ERROR_TEXT = 'Unknown error occurred!'


def get_access_token() -> str:
    """
    Opens browser page to authorize application and asks user to enter
    the received token.

    :return: access token
    """
    print(INSTRUCTIONS_TO_OBTAIN_ACCESS_TOKEN)
    url = VK.auth_url()
    webbrowser.open(url)
    return getpass.getpass(ASK_ACCESS_TOKEN)


def main():
    assert sys.version_info >= (3, 7), "Plyushkin requires Python 3.7+."

    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('--output', default=DEFAULT_OUTPUT,
                        help='output path. Default is "dump"')
    args = parser.parse_args()

    access_token = get_access_token()

    vk = VK(access_token)
    dumper = Dumper(vk, args.output)

    try:
        asyncio.run(dumper.dump())
    except ClientConnectorError as e:
        print(CLIENT_CONNECTION_ERROR_TEXT, e)
        sys.exit(1)
    except IOError as e:
        print(IO_ERROR_TEXT, e)
        sys.exit(1)
    except Exception as e:
        print(UNKNOWN_ERROR_TEXT, e)
        sys.exit(1)


if __name__ == '__main__':
    main()
