from flask import Flask, jsonify, make_response
from vkpymusic import Service
from vkpymusic.models import Song
from vkpymusic.utils import get_logger
from ytmusicapi import YTMusic
from dotenv import load_dotenv
import os
import logging
from tools.get_vk_song_content import get_vk_song_content
from tools.create_yt_search_answer import create_yt_search_answer

app = Flask(__name__)
logger: logging.Logger = get_logger(__name__)

load_dotenv()

user_agent = os.getenv("USER_AGENT")
token_for_audio = os.getenv("TOKEN_FOR_AUDIO")
host = os.getenv("HOST")
port = os.getenv("PORT")


@app.route("/vk/search/<name>", methods=["GET"])
def vk_search(name):
    service = Service(user_agent=user_agent, token=token_for_audio)
    tracks: [Song] = service.search_songs_by_text(name)
    if tracks is None:
        return make_response(jsonify([]), 200)
    songs = []
    for song in tracks:
        song = song.to_dict()
        del song["owner_id"]
        del song["url"]
        song["source"] = "vk"
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
    content = get_vk_song_content(song)
    if content is not None:
        return make_response(content, 200)
    return make_response(
        jsonify({"error": f"content of track with name {track_name} and id {track_id} does not exist"}), 404)


@app.route("/yt/search/<name>", methods=["GET"])
def yt_search(name):
    yt = YTMusic()
    search = yt.search(name, filter="songs")
    length = len(search)
    counter = 3 if length >= 3 else length
    res = [create_yt_search_answer(search[i]) for i in range(counter)]
    return make_response(jsonify(res), 200)


if __name__ == "__main__":
    app.run(host=host, port=port)
