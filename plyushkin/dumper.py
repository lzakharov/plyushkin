import os.path
from pathlib import Path
from typing import List

import aiofiles

from .vk import VK


class Dumper:
    """Dumper is a VK photo dumper."""

    def __init__(self, vk: VK, output: str):
        """
        Create a new dumper.

        :param vk: VK client
        :param output: output directory path
        """
        self.vk = vk

        self.output = output
        if not os.path.exists(self.output):
            os.mkdir(self.output)

    async def dump(self) -> None:
        """
        Dumps user's photo albums and photos in which a user is tagged.
        """
        albums = await self.vk.get_albums()
        await self.dump_albums(albums)

        photos = await self.vk.get_user_photos()
        await self.dump_photos(photos)

    async def dump_albums(self, albums: List[dict]) -> None:
        """Dumps user's photo albums.

        :param albums: albums to dump
        """
        for album in albums:
            await self.dump_album(album)

    async def dump_album(self, album: dict) -> None:
        """
        Creates an album folder and dumps photos there.

        :param album: album to dump
        """
        folder = Path(self.output, album['title'])
        if not os.path.exists(folder):
            os.mkdir(folder)

        photos = await self.vk.get_album_photos(album)
        await self.dump_album_photos(album['title'], photos)

    async def dump_album_photos(
            self,
            album_title: str,
            photos: List[dict],
    ) -> None:
        """
        Dumps the specified album photos.

        :param album_title: album title
        :param photos: album photos to dump
        """
        for photo in photos:
            await self.dump_album_photo(album_title, photo)

    async def dump_album_photo(self, album_title: str, photo: dict) -> None:
        """
        Dumps the specified album photo.

        :param album_title: album title
        :param photo: album photo to dump
        """
        photo_name = await VK.get_photo_name(photo)
        path = Path(
            self.output,
            album_title,
            photo_name
        ).with_suffix(VK.PHOTO_FILE_EXTENSION)

        data = await self.vk.download_photo(photo)

        async with aiofiles.open(path, mode='wb') as f:
            await f.write(data)

    async def dump_photos(self, photos: List[dict]) -> None:
        """
        Creates folder for photos in which a user is tagged and dumps them.

        :param photos: photos in which a user is tagged
        """
        album_title = VK.PHOTOS_OF_ME_ALBUM_TITLE

        folder = Path(self.output, album_title)
        if not os.path.exists(folder):
            os.mkdir(folder)

        for photo in photos:
            await self.dump_album_photo(album_title, photo)
