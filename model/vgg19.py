import torch.nn as nn
from torch import tensor

# ===========
'''
build VGG19
'''
# ===========


def VGG_CBlock(model, layer_nums, in_channels, out_channels, kernel_size=3, stride=1, padding=1):
    """本部分用于组装VGG卷积结构"""
    for _ in range(layer_nums):
        # 每次加入卷积、激活层
        model.append(nn.Conv2d(in_channels=in_channels, out_channels=out_channels,
                               kernel_size=kernel_size, stride=stride, padding=padding))
        model.append(nn.ReLU(inplace=True))
        # 调整通道
        in_channels = out_channels
    # 最后加入最大池化
    model.append(nn.MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False))


def VGG_LBlock(model, args, layer_nums=3, ):
    """本部分用于组装VGG线性结构"""
    for i in range(layer_nums - 1):
        # 除最后一层外，组装入对应的线性层和其他结构
        model.append(nn.Linear(in_features=args[i], out_features=args[i + 1], bias=True))
        model.append(nn.ReLU(inplace=True))
        model.append(nn.Dropout(p=0.5, inplace=False))
    # 醉酒一层只加入线性层
    model.append(nn.Linear(in_features=args[-2], out_features=args[-1], bias=True))


class VGG19(nn.Module):
    def __init__(self):
        super().__init__()

        # 定义特征提取部分
        self.features = nn.Sequential()
        # 所有卷积的最后加入平均池化
        self.avgpool = nn.AdaptiveAvgPool2d(output_size=7, )
        # 定义分类器部分
        self.classifier = nn.Sequential()

        # 放置对应的层
        VGG_CBlock(model=self.features, layer_nums=2, in_channels=3, out_channels=64, )
        VGG_CBlock(model=self.features, layer_nums=2, in_channels=64, out_channels=128, )
        VGG_CBlock(model=self.features, layer_nums=4, in_channels=128, out_channels=256, )
        VGG_CBlock(model=self.features, layer_nums=4, in_channels=256, out_channels=512, )
        VGG_CBlock(model=self.features, layer_nums=4, in_channels=512, out_channels=512, )
        VGG_LBlock(model=self.classifier, layer_nums=3, args=(25088, 4096, 4096, 1000))

    def forward(self, data):
        result = self.features(data)
        result = self.adaavgpool(result)
        result = self.classifier(result)
        return result


class Normalization(nn.Module):
    """这个用来将输入标准化到vgg19的训练输入的分布上，否则vgg19要逼近的真实数据生成分布与输入分布不符合，效能下降"""

    def __init__(self, device, mean=tensor([0.485, 0.456, 0.406]), std=tensor([0.229, 0.224, 0.225])):
        super().__init__()
        # 定义输入的统计量，分离计算图截断梯度流
        self.mean = mean.view(-1, 1, 1).to(device).detach()
        self.std = std.view(-1, 1, 1).to(device).detach()

    def forward(self, img):
        # 定义前向过程：标准化
        return (img - self.mean) / self.std
