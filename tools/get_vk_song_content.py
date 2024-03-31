from vkpymusic.models import Song
from vkpymusic.utils import get_logger
import requests
import logging


def get_vk_song_content(song: Song):
    logger: logging.Logger = get_logger(__name__)
    song.to_safe()
    url = song.url
    if url == "":
        logger.warning("Url no found")
        return
    response = requests.get(url=url)
    if response.status_code == 200:
        if "index.m3u8" in url:
            logger.error(".m3u8 detected!")
            return
        response.close()
        logger.info("Success! Returning music...")
        return response.content
