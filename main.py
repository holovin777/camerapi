import shutil
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import json
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

app = FastAPI()

with open("conf.json", "r") as conf_file:
    site_conf = json.load(conf_file)
    path_to_camera = site_conf["path_to_camera"]
    url = site_conf["url"]
    conf_file.close()

app.mount("/static", StaticFiles(directory=path_to_camera), name="static")

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

articles = os.listdir(path_to_camera)
photos = []
videos = []

@app.get("/")
def read_hello():
    return {"hello": "world"}

@app.get("/photos/scan")
def scan_photos():
    i = 0
    for article in articles:
        if article.endswith(".jpg") or article.endswith(".png"):
            photos.append(
                {
                    "id": i,
                    "url_api": "photos/" + str(i),
                    "name": article,
                    "url_to_photo": url + "static/" + article,
                    "path_to_photo": path_to_camera + article,
                    "url_to_thumbnail": url + "static/" + "thumbnails/" + article + ".thumbnail",
                }
            )
            i = i + 1

    size = 380, 640
    if not os.path.isdir(path_to_camera + "thumbnails"):
        os.mkdir(path_to_camera + "thumbnails")
    for photo in photos:
        with Image.open(photo["path_to_photo"]) as img:
            img.thumbnail(size)
            img.save(path_to_camera + "thumbnails/" + photo["name"] + ".thumbnail", "JPEG")
    thumbnails = os.listdir(path_to_camera + "thumbnails")
    return {"scan_photos": True}

@app.get("/photos")
def read_photos():
    photos_api = []
    for photo in photos:
        photos_api.append(
            {
                "id": photo["id"],
                "name": photo["name"],
                "url": url + photo["url_api"],
                "url_to_thumbnail": photo["url_to_thumbnail"],
            }
        )
    return photos_api

@app.get("/photos/{photo_id}")
async def read_photo(photo_id):
    return {
        "id": photos[int(photo_id)]["id"],
        "name": photos[int(photo_id)]["name"],
        "url_to_photo": photos[int(photo_id)]["url_to_photo"],
        "path_to_photo": photos[int(photo_id)]["path_to_photo"],
        "url_to_thumbnail": photos[int(photo_id)]["url_to_thumbnail"],
    }

@app.get("/videos/scan")
def scan_videos():
    i = 0
    for article in articles:
        if article.endswith(".mp4"):
            videos.append(
                {
                    "id": i,
                    "url_api": "videos/" + str(i),
                    "name": article,
                    "url_to_video": url + "static/" + article,
                    "path_to_video": path_to_camera + article,
                    "url_to_thumbnail": url + "static/" + "thumbnails/" + article + ".thumbnail",
                }
            )
            i = i + 1
    return {"scan_videos": True}

@app.get("/videos")
def read_videos():
    videos_api = []
    for video in videos:
        videos_api.append(
            {
                "id": video["id"],
                "name": video["name"],
                "url": url + video["url_api"],
            }
        )
    return videos_api

@app.get("/videos/{video_id}")
async def read_video(video_id):
    return {
        "id": videos[int(video_id)]["id"],
        "name": videos[int(video_id)]["name"],
        "url_to_video": videos[int(video_id)]["url_to_video"],
        "path_to_video": videos[int(video_id)]["path_to_video"],
    }
