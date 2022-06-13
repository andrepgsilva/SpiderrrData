import json
import uuid
import requests
import os
from dotenv import load_dotenv
load_dotenv()


class MicrosoftTranslate:
    def __init__(self):
        # Add your key and endpoint
        self.key = os.environ.get('TRANSLATE_API_KEY')
        self.endpoint = os.environ.get('TRANSLATE_API_ENDPOINT')

        # Add your location, also known as region. The default is global.
        # This is required if using a Cognitive Services resource.
        self.location = "westeurope"

        self.path = '/translate'
        self.constructed_url = self.endpoint + self.path

        self.params = {
            'api-version': '3.0',
            'from': 'en',
            'to': ['pt']
        }

    def translate(self, textsToTranslate):
        headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            'Ocp-Apim-Subscription-Region': self.location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        # You can pass more than one object in body.
        # body = [{
        #     'text': 'Hello World!'
        # }]

        body = textsToTranslate

        request = requests.post(
            self.constructed_url, params=self.params, headers=headers, json=body)
        response = request.json()

        return json.dumps(response, sort_keys=True,
            ensure_ascii=False, indent=4, separators=(',', ': '))
