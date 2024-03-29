from flask import Flask, jsonify, make_response
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
def vk_search(name):
    service = Service(user_agent=user_agent, token=token_for_audio)
    tracks: [Song] = service.search_songs_by_text(name)
    songs = []
    for song in tracks:
        song = song.to_dict()
        del song["url"]
        songs.append(song)
    return make_response(jsonify(songs), 200)


@app.route("/vk/get/name/<track_name>/track/<track_id>", methods=["GET"])
def vk_get(track_name, track_id):
    service = Service(user_agent=user_agent, token=token_for_audio)
    tracks: [Song] = service.search_songs_by_text(track_name)
    song = None
    for track in tracks:
        if track.track_id == track_id:
            song = track
            break
    if song is None:
        return make_response(jsonify({"error": f"track with name {track_name} and id {track_id} does not exist"}), 404)
    return make_response(jsonify(song.to_dict()), 200)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
