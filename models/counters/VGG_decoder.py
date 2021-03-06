import torch
import torch.nn as nn
import torch.nn.functional as F
from API.layer import Conv2d, FC
from API.util import *
from torchvision import models


class VGG_decoder(nn.Module):
    def __init__(self, pretrained=False):
        super(VGG_decoder, self).__init__()
        vgg = models.vgg16(pretrained=pretrained)
        features = list(vgg.features.children())
        self.features4 = nn.Sequential(*features[0:23])


        self.de_pred = nn.Sequential(Conv2d( 512, 128, 3, same_padding=True, NL='relu'),
                                    nn.ConvTranspose2d(128,64,4,stride=2,padding=1,output_padding=0,bias=True),
                                    nn.ReLU(),
                                    nn.ConvTranspose2d(64,32,4,stride=2,padding=1,output_padding=0,bias=True),
                                    nn.ReLU(),
                                    nn.ConvTranspose2d(32,16,4,stride=2,padding=1,output_padding=0,bias=True),
                                    nn.ReLU(),
                                    Conv2d(16, 1, 1, same_padding=True, NL='relu'))


    def forward(self, x):
        x = self.features4(x)       
        x = self.de_pred(x)

        return x