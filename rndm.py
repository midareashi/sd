import requests
import random
import settings

for i in range(3):
	models = requests.get(url=f'{settings.url}/sdapi/v1/sd-models').json()
	modelrandom = random.randint(0, len(models) - 1)

	option_payload = {
			"sd_model_checkpoint": models[modelrandom].get("title"),
	}

	response = requests.post(url=f'{settings.url}/sdapi/v1/options', json=option_payload)

	with open("generate.py") as f:
			exec(f.read())