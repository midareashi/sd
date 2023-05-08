import requests
import io
import base64
import time
import settings
import payload
from PIL import Image, PngImagePlugin

payload = {
    "prompt": payload.prompt,
    "negative_prompt": payload.negative,
    "steps": 30,
    "width": 512,
    "height": 512,
}

response = requests.post(url=f'{settings.url}/sdapi/v1/txt2img', json=payload)

r = response.json()

for i in r['images']:
    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

    png_payload = {
        "image": "data:image/png;base64," + i
    }
    response2 = requests.post(url=f'{settings.url}/sdapi/v1/png-info', json=png_payload)

    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", response2.json().get("info"))
    imgname = "outputs/img" + str(time.time()) + ".png"
    image.save(imgname, pnginfo=pnginfo)
