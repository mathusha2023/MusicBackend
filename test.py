import requests
from pprint import pprint

vk_host = "http://localhost:8080/vk"


def test(song_name):
    songs = requests.get(vk_host + f"/search/{song_name}").json()
    for song in songs:
        name = song["title"].replace("?", "%3F")
        track_id = song["track_id"]
        full_song = requests.get(vk_host + f"/get/name/{name}/track/{track_id}").json()
        pprint(full_song)
    print("___________________________", end="\n\n\n")


test("Давай расскажем")
test("Я русский")
test("Дед максим")
