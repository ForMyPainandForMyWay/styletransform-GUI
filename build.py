from torch import nn
import loss

from model import vgg19 as real_model

# ========================================================================
"""
This part is writen to build the 'model', 
and count the loss be used to loss of content and style.
The loss will be used by L-BFGS to obtaining images we need.

2023-11-09-yyd
"""


# ========================================================================


def loss_c_and_loss_s_and_model(device, vgg, content_picture,
                                style_picture, weight_c=1,
                                weight_s=1000):
    """组装模型并初始化损失层"""
    # 初始化风格损失容器, 初始话内容损失容器
    style_loss, content_loss = [], []

    # 初始化标准化层，并放到指定设备上再加入模型
    normal = real_model.Normalization(device)
    model = nn.Sequential(normal)
    model_vgg = vgg.to(device)

    # 初始化最初的层数
    layer_number = 1
    # 遍历VGG19的各层，直到超过第五层卷积层
    for name, layer in model_vgg.named_modules():
        # 判断这次遍历到的层是不是卷积层
        if isinstance(layer, nn.Conv2d):
            # 如果是的话判断这一层有没有越界，越界终止循环
            if layer_number <= 5:
                # 把这一层卷积加入网络
                model.append(module=layer)

                # 判断这一层需要计算什么损失
                # 先在当前层的基础上计算出风格图 style_img 在网络中计算出的结果
                output_s = model(style_picture)
                # 先载入风格图，初始化计算风格图的损失的层
                loss_s = loss.Style_loss(style_picture=output_s, weight=weight_s)
                if layer_number != 4:
                    pass
                elif layer_number == 4:
                    # 如果这一层除了风格损失还需要计算内容损失,从模型中分别计算得到风格图与内容图在这一层里的输出
                    output_c = model(content_picture)
                    # 初始化内容损失层
                    loss_c = loss.Content_loss(content_picture=output_c, weight=weight_c)
                    # 损失容器list中加入损失层
                    content_loss.append(loss_c)
                    # 将初始化好的损失层加入模型中
                    model.append(module=loss_c)
                model.append(module=loss_s)
                # 将该损失层放入风格损失的容器list中
                style_loss.append(loss_s)
                # 层数加一
                layer_number += 1

            else:
                # 当遍历越界，退出循环
                break

        # 判断这次遍历到的层是不是池化层
        elif isinstance(layer, nn.MaxPool2d):
            # 加入该池化层
            model.append(layer)

        # 判断这次遍历到的层是不是激活层
        elif isinstance(layer, nn.ReLU):
            # 加入该池化层
            model.append(module=layer)

    model.eval()
    # 返回损失列表和初始化好的model本身
    return content_loss, style_loss, model
