import requests
import settings
import io
import base64
import time
import payload
from PIL import Image, PngImagePlugin

timenow = time.time()
models = requests.get(url=f'{settings.url}/sdapi/v1/sd-models').json()
prompt = payload.prompt
negative = payload.negative

for model in models:
  option_payload = {
    "sd_model_checkpoint": model.get("title"),
  }

  response = requests.post(url=f'{settings.url}/sdapi/v1/options', json=option_payload)

  payload = {
    "prompt": prompt,
    "negative_prompt": negative,
    "steps": 10,
    "width": 512,
    "height": 512,
    "seed": timenow,
    "cfg_scale": 7,
    "sampler_name": "DPM++ SDE Karras",
  }

  print("Creating image for " + model.get("title") + ".")

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
    imgname = "outputs/img" + str(timenow) + "-" + str(model.get("title")) + ".png"
    image.save(imgname, pnginfo=pnginfo)
