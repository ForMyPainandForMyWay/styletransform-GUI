import torch
from torch import nn

# ======================================================================================================================
"""
This part will define the Content loss and Style loss,
gram matrix will be defined too, and it will be used to count the style representation.
By the rep... we cen get the loss of style, and we can optim the target img.
Every part must rewrite the method 'forward' and 'backward', so we can use them as a layer, 
and then you can use some functions to derive them when you need to 'backward' the target.
Remember, this part ues a func called tensor.detach(), 
this is to makesure some tensor will not be calculated gradient(we call this operation to '将变量分理出计算图')

2023-11-09-yyd
"""


# ======================================================================================================================

class Content_loss(nn.Module):
    """定义内容损失计算层"""

    def __init__(self, content_picture, weight):
        super().__init__()
        # 初始化损失
        self.loss = None
        # 初始化内容图，将传入的内容图分理出计算图，以免对其求导
        self.content_picture = content_picture.detach()
        # 初始化权重
        self.weight = weight
        # 初始化计算方式
        self.criterion = nn.MSELoss()

    def forward(self, input_):
        # 定义前向传播过程：计算损失，返回传入的原图
        self.loss = self.criterion(input_ * self.weight, self.content_picture)
        # 输出输入的副本，在后续过程对这个副本进行计算loss，防止在后续计算过程中对input进行卷积等计算导致梯度计算报错
        return input_.clone()

    def backward(self):
        # 定义反向传播过程，反向传播并计算梯度，保存计算图，否则会出错
        self.loss.backward(retain_graph=True)
        # 输出loss方便后面对多个loss进行优化
        return self.loss


class Gram(nn.Module):
    """定义GRAM矩阵用来表示风格"""

    def __init__(self, ):
        super().__init__()
        # self.feature_map = feature_map

    def forward(self, feature_map):
        # 定义前向过程
        # 获取张量大小
        batch_size, depth, l, w = feature_map.size()

        feature_matrix = feature_map.reshape(batch_size * depth, l * w)  # 将多层特征图扁平化成一个二维图，每层特征图展开成每行
        gram = torch.mm(feature_matrix, feature_matrix.t())  # 使用mm计算矩阵乘法高效地间接计算内积，求出gram矩阵
        # 逐个归一化元素
        return gram.div(batch_size * depth * l * w)


class Style_loss(nn.Module):
    """定义风格损失"""

    def __init__(self, style_picture, weight):
        super().__init__()
        self.weight = weight  # 风格损失权重
        self.gram = Gram()  # 初始化gram
        self.style_gram = Gram()  # 初始化风格gram
        self.style_picture = style_picture.detach()  # 分离计算图
        self.criterion = nn.MSELoss()  # 初始化损失函数

    def forward(self, input_):
        gram = self.gram(input_) * self.weight
        # 前向传播时计算损失
        self.loss = self.criterion(gram, self.style_gram(self.style_picture).detach() * self.weight)
        # 返回副本，防止后续卷积池化等操作对梯度计算产生影响
        return input_.clone()

    def backward(self):
        # 反向过程进行梯度计算
        self.loss.backward(retain_graph=True)
        # 反向过程返回loss
        return self.loss
