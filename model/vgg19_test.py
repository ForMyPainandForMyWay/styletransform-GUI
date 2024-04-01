import torch.nn as nn


class VGG19(nn.Module):
    def __init__(self):
        super().__init__()
        inplace = True

        self.features = nn.Sequential()
        self.avgpool = nn.AdaptiveAvgPool2d(output_size=7, )
        self.classifier = nn.Sequential()

        self.features.append(nn.Conv2d(in_channels=3, out_channels=64, kernel_size=3, stride=1, padding=1, ))
        self.features.append(nn.ReLU(inplace=inplace))
        self.features.append(nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1, padding=1))
        self.features.append(nn.ReLU(inplace=inplace))
        self.features.append(nn.MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False))

        self.features.append(nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1))
        self.features.append(nn.ReLU(inplace=inplace))
        self.features.append(nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, stride=1, padding=1))
        self.features.append(nn.ReLU(inplace=inplace))
        self.features.append(nn.MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False))

        self.features.append(nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, stride=1, padding=1))
        self.features.append(nn.ReLU(inplace=inplace))
        self.features.append(nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1))
        self.features.append(nn.ReLU(inplace=inplace))
        self.features.append(nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1))
        self.features.append(nn.ReLU(inplace=inplace))
        self.features.append(nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1))
        self.features.append(nn.ReLU(inplace=inplace))
        self.features.append(nn.MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False))

        self.features.append(nn.Conv2d(in_channels=256, out_channels=512, kernel_size=3, stride=1, padding=1))
        self.features.append(nn.ReLU(inplace=inplace))
        self.features.append(nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        self.features.append(nn.ReLU(inplace=inplace))
        self.features.append(nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        self.features.append(nn.ReLU(inplace=inplace))
        self.features.append(nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        self.features.append(nn.ReLU(inplace=inplace))
        self.features.append(nn.MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False))

        self.features.append(nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        self.features.append(nn.ReLU(inplace=inplace))
        self.features.append(nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        self.features.append(nn.ReLU(inplace=inplace))
        self.features.append(nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        self.features.append(nn.ReLU(inplace=inplace))
        self.features.append(nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        self.features.append(nn.ReLU(inplace=inplace))
        self.features.append(nn.MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False))

        self.classifier.append(nn.Linear(in_features=25088, out_features=4096, bias=True))
        self.classifier.append(nn.ReLU(inplace=inplace))
        self.classifier.append(nn.Dropout(p=0.5, inplace=False))
        self.classifier.append(nn.Linear(in_features=4096, out_features=4096, bias=True))
        self.classifier.append(nn.ReLU(inplace=inplace))
        self.classifier.append(nn.Dropout(p=0.5, inplace=False))
        self.classifier.append(nn.Linear(in_features=4096, out_features=1000, bias=True))

    def forward(self, data):
        result = self.features(data)
        result = self.adaavgpool(result)
        result = self.classifier(result)
        return result
