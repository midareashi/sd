import requests
import io
import base64
import time
import settings
from PIL import Image, PngImagePlugin

payload = {
    "prompt": "create a visually captivating scene in a barren and desolate alien desert landscape. Within this harsh world, depict a young woman with highly defined pale blue skin, hovering effortlessly approximately 1 meter above the ground. Despite the unforgiving environment, her face is adorned with a genuine smile and her eyes sparkle with happiness and optimism. The alien desert stretches out in all directions, with jagged rock formations and sandy dunes that seem to go on endlessly. The land is devoid of vegetation, and the earth is cracked and parched, reflecting the unforgiving nature of the world she inhabits. The vast expanse of the desert adds a sense of isolation and mystery to the scene. Amidst this desolation, the young woman stands out like a beacon of hope. Her defined pale blue skin stands in contrast to the barren surroundings, emphasizing her resilience and inner strength. Her body, with its intricate details and contours, reflects the determination and beauty that thrives even in adversity. She wears a knee-length dress in pale blue, a vibrant hue that serves as a symbol of her optimism and vibrant spirit. The fabric transforms into wisps of smoke at the bottom, as if embracing the harsh environment while retaining its ethereal qualities. Her flowing pale blue hair cascades down, transforming into delicate tendrils of smoke at the ends, symbolizing her ability to find joy and beauty even in the harshest of circumstances. Let the lighting be stark and dramatic, casting long shadows across the barren desert landscape. The sun, blazing in the sky, adds a touch of warmth to the scene, contrasting with the desolation and highlighting the young woman's resilience and unwavering positivity. As viewers gaze upon the image, they are drawn into a world where happiness and optimism exist despite the adversities of the environment. The young woman's radiant spirit and unwavering cheer inspire viewers to find joy and hope even in the most challenging circumstances. Embrace your artistic vision and create a captivating masterpiece that juxtaposes the harshness of the alien desert with the transformative power of happiness and optimism.",
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
