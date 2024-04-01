def create_yt_search_answer(song: dict):
    d = {}
    artists = [i["name"] for i in song["artists"]]
    d["artist"] = ", ".join(artists)
    d["duration"] = song["duration_seconds"]
    d["title"] = song["title"]
    d["track_id"] = song["videoId"]
    return d
