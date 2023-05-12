import requests
import config.settings as settings
import io
import base64
import time
import config.payload as payload
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
    "steps": 30,
    "width": 1024,
    "height": 768,
    "seed": timenow,
    "cfg_scale": 9,
    "sampler_name": "DPM++ SDE Karras",
  }

  print("Creating image for " + str(model.get("model_name")) + ". Number " + str(models.index(model) + 1) + " of " + str(len(models)) + ".")

  response = requests.post(url=f'{settings.url}/sdapi/v1/txt2img', json=payload)

  r = response.json()

  for i in r['images']:
    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

    png_payload = {
      "image": "data:image/png;base64," + i
    }
    response2 = requests.post(url=f'{settings.url}/sdapi/v1/png-info', json=png_payload)

    #print(response2.json().get("info"))

    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", response2.json().get("info"))
    imgname = "outputs/" + str(model.get("model_name")) + "-" + str(timenow) + ".png"
    image.save(imgname, pnginfo=pnginfo)
