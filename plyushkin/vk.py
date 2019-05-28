from typing import List
from urllib.parse import urlencode, urljoin

import aiohttp as http

APPLICATION_ID = 6996201


class VK:
    """VK client."""

    OAUTH_URL = 'https://oauth.vk.com/authorize'
    OAUTH_DISPLAY = 'page'
    OAUTH_REDIRECT_URI = 'https://oauth.vk.com/blank.html'
    OAUTH_SCOPE = 'photos'
    OAUTH_RESPONSE_TYPE = 'token'

    API_URL = 'https://api.vk.com'
    API_VERSION = '5.95'

    GET_ALBUMS_URL = urljoin(API_URL, 'method/photos.getAlbums')
    GET_ALBUM_PHOTOS_URL = urljoin(API_URL, 'method/photos.get')
    GET_USER_PHOTOS = urljoin(API_URL, 'method/photos.getUserPhotos')
    GET_PHOTOS_MAX_COUNT = 1000

    PHOTOS_OF_ME_ALBUM_TITLE = 'Photos of me'

    PHOTO_FILE_EXTENSION = '.png'
    PHOTO_TYPES = ['s', 'm', 'x', 'o', 'p', 'q', 'r', 'y', 'z', 'w']
    PHOTO_TYPE_VALUE = {x: i for i, x in enumerate(PHOTO_TYPES)}

    def __init__(self, access_token: str):
        """
        Create a new VK client.

        :param access_token: VK user access token
        """
        self.access_token = access_token

    @property
    def base_params(self) -> dict:
        """
        Contains base request parameters.

        :return: base request parameters
        """
        params = {
            'v': VK.API_VERSION,
            'access_token': self.access_token,
        }
        return params

    @staticmethod
    def auth_url() -> str:
        """
        Creates a VK authorization URL.

        :return: VK authorization URL
        """
        params = urlencode({
            'client_id': APPLICATION_ID,
            'display': VK.OAUTH_DISPLAY,
            'redirect_uri': VK.OAUTH_REDIRECT_URI,
            'scope': VK.OAUTH_SCOPE,
            'response_type': VK.OAUTH_RESPONSE_TYPE,
        })

        return f'{VK.OAUTH_URL}?{params}'

    @staticmethod
    async def get_photo_name(photo: dict) -> str:
        """
        Gets a photo name.

        :param photo: photo
        :return: photo name
        """
        return str(photo['id'])

    @staticmethod
    async def get_resp_items(resp: dict) -> List[dict]:
        """
        Gets response items.

        :param resp: response
        :return: items
        """
        return resp['response']['items']

    async def get_json(self, url: str, params: dict) -> dict:
        """
        Makes http request and returns JSON response data.

        :param url: URL
        :param params: request parameters
        :return: JSON response data
        """
        params.update(self.base_params)
        async with http.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                data = await resp.json()

        return data

    async def get_bytes(self, url: str, params: dict) -> bytes:
        """
        Makes http request and returns bytes response data.

        :param url: URL
        :param params: request parameters
        :return: response data in bytes
        """
        params.update(self.base_params)
        async with http.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                data = await resp.read()

        return data

    async def get_items(self, url: str, params: dict) -> List[dict]:
        """
        Makes http request and returns items from JSON response data.

        :param url: URL
        :param params: request parameters
        :return: items
        """
        result = []

        params.update({
            'count': VK.GET_PHOTOS_MAX_COUNT,
            'offset': 0,
        })

        while True:
            data = await self.get_json(url, params)
            items = await self.get_resp_items(data)
            if not items:
                break

            result.extend(items)
            params['offset'] += VK.GET_PHOTOS_MAX_COUNT

        return result

    async def get_albums(self) -> List[dict]:
        """
        Gets VK user albums.

        :return: list of albums
        """
        albums = await self.get_items(VK.GET_ALBUMS_URL, {})
        return albums

    async def get_album_photos(self, album: dict) -> List[dict]:
        """
        Gets VK user album photos.

        :return: list of album photos
        """
        params = {
            'album_id': album['id'],
        }

        photos = await self.get_items(VK.GET_ALBUM_PHOTOS_URL, params)
        return photos

    async def get_user_photos(self) -> List[dict]:
        """
        Gets VK user photos in which a user is tagged.

        :return: list of photos
        """
        photos = await self.get_items(VK.GET_USER_PHOTOS, {})
        return photos

    async def download_photo(self, photo: dict) -> bytes:
        """
        Downloads specified photo with max resolution.

        :param photo: photo to download
        :return: downloaded photo content in bytes
        """
        max_photo = max(photo['sizes'],
                        key=lambda x: VK.PHOTO_TYPE_VALUE[x['type']])
        url = max_photo['url']
        content = await self.get_bytes(url, {})
        return content
