import requests
import json
import base64
with open("./static/datasets/SHHB/2.jpg", "rb") as imageFile:
        str_byte = base64.b64encode(imageFile.read())
json_data = {
    'model':'alexnet',
    'image': str_byte
}
data = requests.post('http://127.0.0.1:5000/pred',data=json_data)
print(data.content)