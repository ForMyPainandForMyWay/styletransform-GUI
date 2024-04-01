import build
import read_img
from model.vgg19 import VGG19
from model.mini_vgg19 import Mini_VGG19
from torch import load

from torch import randn
from torch import cat
from torch.optim import LBFGS
from torchvision import transforms
from time import perf_counter
from torch.utils import tensorboard
import numpy as np

# ===================================================================================================
'''
This part is designed for GUI running, based on build.py.
The 1st vision did not encapsulate the following code into a class.
Each loss will be used to perform second-order optimization(L-BFGS).
The calculation process of loss similar as a 'Concurrent' process(actually, it's not).

2023.11.09-yyd
'''


# ===================================================================================================


class Transfer:
    """完成并打包风格迁移过程"""

    def __init__(self, path_s, path_c, method='mini', weight_c=1, weight_s=1000, time=10, ph_name='result.png'):
        # 初始化记录状态的对象，设置其文件夹为logs
        self.writer = tensorboard.SummaryWriter('logs')
        # 设置迭代时间
        self.time = time
        # 初始化计算图像
        self.style_picture, self.device = read_img.r_img(path_s)
        # 初始化内容图像与目标图像，这里不采用高斯噪声图像而直接使用内容图作为初始目标图
        self.content_picture, _ = read_img.r_img(path_c)
        self.content_picture = self.content_picture.to(self.device)
        self.input_picture = self.content_picture.clone().requires_grad_(True)
        # 初始化各损失所占权重
        self.weight_alpha = weight_c
        self.weight_beta = weight_s
        # LBFGS算法先传入一个需要反向传播的variable，然后传入一个返回值为损失的闭包
        self.optimizer = LBFGS([self.input_picture])
        # 目标图像的名字
        self.ph_name = ph_name

        # 调用vgg19结构
        if method == 'mini':
            self.vgg = Mini_VGG19()
            # 指定参数加载路径
            pre_file = load(r".\model\mini_vgg19.pth")
        else:
            self.vgg = VGG19()
            pre_file = load(r".\model\vgg19.pth")
        # 结构载入参数
        self.vgg.load_state_dict(pre_file)
        # 载入测试模式
        self.vgg.eval()

    def start(self):
        """这部分用来执行计算"""
        # 初始化对象，获取内容损失风格损失的列表，model，设备
        loss_c, loss_s, model = build.loss_c_and_loss_s_and_model(content_picture=self.content_picture,
                                                                  style_picture=self.style_picture,
                                                                  device=self.device, vgg=self.vgg)
        # 伪造输入&将model的计算图加入SummaryWriter中
        self.writer.add_graph(model=model, input_to_model=randn(1, 3, 512, 512).to(self.device))
        # 初始化计算所用时间
        time = 0
        # 设置时间标记，记下迭代前的时间
        start = perf_counter()
        # 初始化迭代步
        i = 0
        # 当计算总时间没有超过预设时间限制时进行迭代
        while time <= self.time:
            # 为了使用L拟牛顿法，将计算梯度的过程放入一个函数中传给LBFGS
            def func():
                # 梯度归0
                self.optimizer.zero_grad()
                # 初始化损失值
                loss_style, loss_content = 0, 0
                # 将张量归一化（防止异常大小的像素值）覆盖原张量
                self.input_picture.data.clamp_(0, 1)
                # model前向传播
                model(self.input_picture)

                # 遍历内容损失，计算梯度，同时返回并累计内容损失
                for loss_ in loss_s:
                    loss_style += loss_.backward()

                for loss_ in loss_c:
                    loss_content += loss_.backward()

                # 将损失写入日志
                self.writer.add_scalar(tag='loss' + str(start),
                                       scalar_value=loss_style + loss_content,
                                       global_step=i)

                return loss_style + loss_content

            # 优化器传入函数进行迭代优化
            self.optimizer.step(closure=func)
            # 日志记录每一次迭代的计算结果
            self.writer.add_image(tag='output' + str(start),
                                  img_tensor=np.array(transforms.ToPILImage()(cat((self.content_picture,
                                                                                   self.input_picture,
                                                                                   self.style_picture),
                                                                                  dim=3).cpu().squeeze(0))),
                                  dataformats='HWC',
                                  global_step=i)
            i += 1
            # 更新耗时
            end = perf_counter()
            time = end - start
        # 关闭日志记录
        self.writer.close()

        # 删除0维batch_size
        self.save_pic = transforms.ToPILImage()(self.input_picture.cpu().squeeze(0))
        # 最后一次进行输出归一化
        self.input_picture.data.clamp_(0, 1)
        # 储存存图像
        self.save_pic.save(self.ph_name)  # 保存图像
        print(time)
        # 返回文件地址
        return './' + self.ph_name
