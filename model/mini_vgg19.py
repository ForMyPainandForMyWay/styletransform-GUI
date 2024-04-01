from torch import nn


class Mini_VGG19(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential()
        self.model.append(nn.Conv2d(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)))
        self.model.append(nn.ReLU(inplace=True))
        self.model.append(nn.Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)))
        self.model.append(nn.ReLU(inplace=True))
        self.model.append(nn.MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False))
        self.model.append(nn.Conv2d(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)))
        self.model.append(nn.ReLU(inplace=True))
        self.model.append(nn.Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)))
        self.model.append(nn.ReLU(inplace=True))
        self.model.append(nn.MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False))
        self.model.append(nn.Conv2d(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)))
        self.model.append(nn.ReLU(inplace=True))

    def forward(self, data):
        return self.model(data)
