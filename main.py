from flask import Flask, jsonify
from vkpymusic import Service
from vkpymusic.models import Song
from vkpymusic.utils import get_logger
from dotenv import load_dotenv
import os
import logging

app = Flask(__name__)
logger: logging.Logger = get_logger(__name__)

load_dotenv()

user_agent = os.getenv("USER_AGENT")
token_for_audio = os.getenv("TOKEN_FOR_AUDIO")


@app.route("/vk/search/<name>", methods=["GET"])
def search(name):
    service = Service(user_agent=user_agent, token=token_for_audio)
    tracks: [Song] = service.search_songs_by_text(name)
    songs = []
    for song in tracks:
        song = song.to_dict()
        del song["owner_id"]
        del song["url"]
        songs.append(song)
    return jsonify(songs)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
