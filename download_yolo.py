import urllib.request
import os

def download_yolo():
    os.makedirs("models", exist_ok=True)
    model_path = "models/yolov8n.pt"
    if not os.path.exists(model_path):
        url = "https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt"
        print(f"Downloading {url} to {model_path}...")
        try:
            # Add user agent to avoid 403
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(model_path, 'wb') as out_file:
                out_file.write(response.read())
            print("Download successful.")
        except Exception as e:
            print(f"Failed to download: {e}")
    else:
        print("Model already exists.")

if __name__ == "__main__":
    download_yolo()
