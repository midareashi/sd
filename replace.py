import requests
import io
import base64
import time
import config.settings as settings
from PIL import Image, PngImagePlugin

names = ["shift","a-line","sheath","bodycon","tent","empire","strapless","halter","1-shoulder","apron","jumper","sun","wrap","pouf","slip","qi pao","shirt","maxi","ball gown","little black"]
timenow = time.time()

for name in names:
  payload = {
    "prompt": """
      Create a photo-realistic AI-generated image capturing the youthful beauty of Syl, the enchanting spren from the Stormlight Archive series by Brandon Sanderson. Syl should be depicted as a vibrant and youthful figure, with an appearance resembling that of a 16-year-old. Her youthful features should exude a sense of innocence, curiosity, and wonder.

      Syl should be portrayed floating gracefully in mid-air, with a height of one meter above the ground. Her attire should consist of a modest knee-length apron dress in a delicate pale blue color. The dress should embody simplicity and elegance, reflecting her ethereal nature.

      Her hair, resembling mist, should cascade around her in a playful and dynamic manner. Its pale blue hue should further enhance her mystical presence. The mist-like essence from her hair and dress should create an enchanting visual effect, adding to the overall magical atmosphere of the image.

      The background should depict a serene and enchanting setting, such as a sunlit meadow or a picturesque woodland. Soft sunlight filtering through the trees should illuminate the scene, casting a gentle glow on Syl's youthful form. The image should convey a sense of joy, freedom, and the unbounded energy of youth.

      This image aims to capture Syl's youthful charm and ethereal nature, emphasizing her connection to the mystical world of Roshar. Through her appearance and the serene surroundings, the image should evoke a sense of enchantment and wonder.
    """,
    "negative_prompt": "paintings, sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, glans, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, glans,extra fingers,fewer fingers,strange fingers,bad hand (low quality, worst quality:1.4), (bad_prompt:0.8), (monochrome), (greyscale), (nsfw:1.8)",
    "steps": 20,
    "width": 512,
    "height": 512,
    "seed": timenow,
    "sampler_index": "Euler A",
    "restore_faces": True,
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
