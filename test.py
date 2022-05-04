import requests
import base64
import matplotlib.pyplot as plt
import os
# with open("./static/datasets/SHHB/2.jpg", "rb") as imageFile:
#         str_byte = base64.b64encode(imageFile.read())
folder = 'static/datasets/SHHA'
imgs = os.listdir(folder)
for file in imgs:
    if file.endswith(".jpg"):
        json_data = {
            'model':'alexnet',
            'image': folder + "/" + file
        }
        print(json_data)
        plt.subplot(2,1,1)
        img = plt.imread(json_data['image'])
        plt.imshow(img)
        data = requests.post('http://127.0.0.1:5000/predict',data=json_data)
        print(data.content)
        plt.subplot(2,1,2)
        d_map = plt.imread('./static/map.jpg')
        plt.imshow(d_map)
        plt.show(block=True)