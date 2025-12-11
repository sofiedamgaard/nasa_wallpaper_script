import os, requests
from pathlib import Path
from datetime import date
import subprocess

def get_data(api_key, date=None, timeout=60):
    params = {"api_key": api_key}
    if date:
        params["date"] = date
    r = requests.get("https://api.nasa.gov/planetary/apod", params=params, timeout=timeout)
    r.raise_for_status()
    return r.json()

def get_date(response): return response.get("date")

def get_hdurl(response): return response.get("hdurl")

def get_url(response): return response.get("url")

def get_media_type(response): return response.get("media_type")

def get_service_version(response): return response.get("service_version")

def get_explanation(response): return response.get("explanation")

def get_title(response): return response.get("title")

def get_image_url(response):
    if get_media_type(response) != "image":
        return None
    return get_hdurl(response) or get_url(response)

def download_image(url, stem, out_dir=Path(".")):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    jpg_path = out_dir / f"{stem}.jpg"

    if jpg_path.exists():
        return None
    
    r = requests.get(url, timeout=60)
    r.raise_for_status()

    if "image" not in r.headers.get("Content-Type", ""):
        raise ValueError("URL did not return an image content type")
    
    jpg_path.write_bytes(r.content)
    return jpg_path

def set_wallpaper(path):
    subprocess.run(["wallpaper", "set", str(path)], check=True)
    print("wallpaper set on all screens")

def run(api_key, date=None, out_dir=Path(".")):
    resp = get_data(api_key, date=date)
    date = get_date(resp)
    title = get_title(resp)
    img_url = get_image_url(resp)

    if not img_url:
        print(f"{date}: Not an image (media_type={get_media_type(resp)})")
        return
    
    out_dir = Path(out_dir)
    path = download_image(img_url, date, out_dir=out_dir)
    
    if path is None:
        path = out_dir / f"{date}.jpg"
        print(f"{date}: Image already exists in {out_dir} as {date}")
    else:    
        print(f"Saved JPG to {path}. Title: {title}")

    set_wallpaper(path)
 
if __name__ == "__main__":
    API_KEY = os.getenv("NASA_API_KEY")
    if not API_KEY:
        raise RuntimeError("error: Environment variable NASA_API_KEY is not set")
    today = date.today()
    run(API_KEY, today, out_dir="images")