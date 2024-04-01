from torchvision import transforms
import torch
import PIL.Image as PI

# ================================================
"""
# This part is for reading the img.

2023-11-09-yyd 
"""
# ================================================


def r_img(path):
    # 判断设备是否具备GPU加速能力
    if torch.cuda.is_available():
        # 指定加速计算设备，并指定图片裁剪大小
        device = 'cuda:0'
        img_size = 512, 512
    else:
        # 指定计算设备为cpu，并计算图片裁剪大小
        device = 'cpu'
        img_size = 128

    # 定义图片预处理以及读取器
    img = PI.open(path).convert(mode='RGB')  # 把RGBA或者其他什么模式的图转成三通道的RGB
    tf = transforms.Compose([transforms.ToTensor(), transforms.Resize(img_size)])  # 定义图片预处理过程
    img = tf(img)  # 预处理
    img = img.unsqueeze(0).to(device)  # 放到指定设备上，并增加一个表示batch_size的0维度，用来匹配网络输入
    return img, device
