import torch
import torch.nn as nn
from torch.hub import load_state_dict_from_url

from copy import deepcopy


__all__ = ['AlexNet_dann', 'alexnet_dann']


model_urls = {
    'alexnet': 'https://download.pytorch.org/models/alexnet-owt-4df8aa71.pth',
}


class AlexNetDANN(nn.Module):

    def __init__(self, num_classes=1000):
        super(AlexNetDANN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=11, stride=4, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(64, 192, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(192, 384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )
        self.avgpool = nn.AdaptiveAvgPool2d((6, 6))
        self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes),
        )
        self.domainClassifier = nn.Sequential()

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x


    def alexnet_dann(pretrained=False, progress=True, **kwargs):
        model = AlexNetDANN(**kwargs)
        if pretrained:
            state_dict = load_state_dict_from_url(model_urls['alexnet'],
                                              progress=progress)
            model.load_state_dict(state_dict)
        
        model.domainClassifier = deepcopy(model.classifier)
    
        model.classifier[6] = nn.Linear(4096, 7)
        model.domainClassifier[6] = nn.Linear(4096, 2)
    
        return model
