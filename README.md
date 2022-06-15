# camerapi
Api for Camera

## Installation
```bash
git clone https://github.com/holovin777/camerapi.git
cd camerapi
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
vim conf.json
```
```json
{"path_to_camera": "/home/admin/Camera/", "url": "http://localhost:8000/"}
```
```bash
uvicorn main:app --reload
```
