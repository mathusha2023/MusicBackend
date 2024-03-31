import requests

vk_host = "http://localhost:8080/vk"


def test(song_name):
    songs = requests.get(vk_host + f"/search/{song_name}").json()
    print(songs)
    for song in songs:
        name = song["title"].replace("?", "%3F")
        track_id = song["track_id"]
        response = requests.get(vk_host + f"/get/name/{name}/track/{track_id}")
        with open(f"{name} {track_id}.mp3", "wb") as f:
            f.write(response.content)
    print("___________________________", end="\n\n\n")


test("Давай расскажем")
test("Я русский")
test("Дед максим")
