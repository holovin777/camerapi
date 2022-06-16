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
i = 0

for article in articles:
    if article.endswith(".jpg") or article.endswith(".png"):
        photos.append(
            {
                "id": i,
                "name": article,
                "url_to_photo": url + "static/" + article,
                "path_to_photo": path_to_camera + article,
                "url_to_thumbnail": url + "static/" + "thumbnails/" + article + ".thumbnail",
            }
        )
        i = i+1

for article in articles:
    if article.endswith(".mp4"):
        videos.append({"id": i, "path_to_video": url+"static/"+article})
        i = i+1

@app.get("/")
def read_hello():
    return {"hello": "world"}

@app.get("/photos")
def read_photos():
    size = 380, 640
    if not os.path.isdir(path_to_camera + "thumbnails"):
        os.mkdir(path_to_camera + "thumbnails")
    for photo in photos:
        with Image.open(photo["path_to_photo"]) as img:
            img.thumbnail(size)
            img.save(path_to_camera + "thumbnails/" + photo["name"] + ".thumbnail", "JPEG")
    thumbnails = os.listdir(path_to_camera + "thumbnails")
    thumbnails.sort(reverse=True)
    return photos

@app.get("/videos")
def read_videos():
    return videos
