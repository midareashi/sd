import requests
import settings

models = requests.get(url=f'{settings.url}/sdapi/v1/sd-models').json()

for model in models:
	option_payload = {
			"sd_model_checkpoint": model.get("title"),
	}

	response = requests.post(url=f'{settings.url}/sdapi/v1/options', json=option_payload)

	with open("generate.py") as f:
			exec(f.read())
