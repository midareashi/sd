import requests
import io
import base64
import time
import settings
from PIL import Image, PngImagePlugin

names = ["shift","a-line","sheath","bodycon","tent","empire","strapless","halter","1-shoulder","apron","jumper","sun","wrap","pouf","slip","qi pao","shirt","maxi","ball gown","little black"]
timenow = time.time()

for name in names:
  payload = {
    "prompt": """
      Create a photo-realistic image depicting a woman exuding confidence and grace as she walks along a vibrant city sidewalk. The woman should be wearing a (""" + name + """ dress:1.6) that accentuates her figure, paired with stylish high heels. The setting should showcase a bustling urban environment, with skyscrapers, bustling traffic, and a lively atmosphere. Capture the moment when the woman's stride is at its peak, conveying a sense of poise and purpose. The image should evoke a blend of sophistication, fashion, and the vibrant energy of city life.
    """,
    "negative_prompt": "paintings, sketches, (worst quality:2), (low quality:2), (normal quality:2), normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, glans, (worst quality:2), (low quality:2), (normal quality:2), normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, glans, extra fingers, fewer fingers, strange fingers, bad hand (low quality, worst quality:1.4), (bad_prompt:0.8), (monochrome), (greyscale), (nsfw:1.8)",
    "steps": 20,
    "width": 512,
    "height": 512,
    "seed": timenow,
  }

  print("Creating image for " + name + ". Number " + str(names.index(name) + 1) + " of " + str(len(names)) + ".")

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
    imgname = "outputs/img" + str(timenow) + "-" + str(names.index(name) + 1) + "-" + name + ".png"
    image.save(imgname, pnginfo=pnginfo)
