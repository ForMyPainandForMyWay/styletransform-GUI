import os
import stat
import shutil
from transfer_ui import Ui_Form
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QApplication, QInputDialog, QLineEdit, QFileDialog, QWidget

from run import Transfer


class Stats(QWidget, Ui_Form):
    def __init__(self):
        # 安装窗体
        super().__init__()
        self.setupUi(self)

        # 定义一个异常响应窗口
        self.error_box = QtWidgets.QMessageBox()
        # 定义一个提示clear结果的窗口
        self.clear_box = QtWidgets.QMessageBox()

        # 初始化控件
        self.init()

        # 设置初始时间限制
        self.time = 15

    def init(self):
        """按钮初始化：绑定按钮行为"""
        # 绑定input_picture按钮的行为
        self.show_picture.clicked.connect(self.input_img)
        # 绑定shou_picture按钮的行为
        self.show_picture_2.clicked.connect(self.show_img)
        # 绑定时间设置按钮的行为
        self.set_time.clicked.connect(self.s_e)
        # 以下两行绑定展示图片的两个按钮的行为
        self.c_t_b.clicked.connect(self.get_path_c)
        self.s_t_b.clicked.connect(self.get_path_s)
        # 绑定clear按钮的行为
        self.Clear.clicked.connect(self.clear_logs)

        # 设置按钮颜色
        self.show_picture.setStyleSheet("background-color:#81FBB8")
        self.show_picture_2.setStyleSheet("background-color:#FFD26F")
        self.set_time.setStyleSheet("background-color:#81FFEF")

        # 设置显示区默认背景
        self.content_img.setPixmap(QtGui.QPixmap('./ph/C.png'))
        self.style_img.setPixmap(QtGui.QPixmap('./ph/S.png'))
        self.result_img.setPixmap(QtGui.QPixmap('./ph/R.png'))

        # 设置异常响应窗口的名字
        self.error_box.setWindowTitle('Error')
        # 设置异常响应的内容
        self.error_box.setText('Something is error, check your input.')

        # 设置clear提示窗口
        self.clear_box.setWindowTitle('log clear')
        # 设置窗口内容
        self.clear_box.setText('The log has been cleared')

    def input_img(self):
        """根据地址框放入的地址显示并绑定图片"""
        try:
            # 首先将地址框的地址正确转义
            self.address_content_img_ = self.address_content_img.toPlainText().replace('\\', '/')
            self.address_style_img_ = self.address_style_img.toPlainText().replace('\\', '/')
            # 如果前后有引号去掉引号
            set_ = {"'", '‘', '"', '”', '“'}
            if (self.address_content_img_[0] in set_) and (self.address_content_img_[-1] in set_):
                self.address_content_img_ = self.address_content_img_[1:-1]
            if (self.address_style_img_[0] in set_) and (self.address_style_img_[-1] in set_):
                self.address_style_img_ = self.address_style_img_[1:-1]
            # 绑定图片
            self.content = QtGui.QPixmap(self.address_content_img_)
            self.style = QtGui.QPixmap(self.address_style_img_)

            # 把要计算的图片放到相应位置显示
            self.content_img.setPixmap(self.content)
            self.style_img.setPixmap(self.style)
        except:
            # 异常处理
            self.error_act()

    def show_img(self):
        """展示并计算图片"""
        try:
            # 构建迁移的对象
            self.transfer = Transfer(path_s=self.address_style_img_, path_c=self.address_content_img_,
                                     time=self.time, method='mini')

            # 执行计算，并将生成的图片的临时路径路径返回
            path = self.transfer.start()
            # 获取新路径
            new_path = self.get_save_path()
            # 改名并移动
            if new_path != '':
                os.rename(path, new_path)
                path = new_path
            else:
                pass
                # 获取result图片
            self.result_qpixmap = QtGui.QPixmap(path)
            # 展示结果图片
            self.result_img.setPixmap(self.result_qpixmap.scaled(451, 271))
        except:
            self.error_act()

    def s_e(self):
        """设置迭代时间"""
        # 使用输入窗口获取要修改的时间
        self.time, okPressed = QInputDialog.getText(self, 'set time',
                                                    '警告：请慎重选择计算时间\nGPU: 3070ti '
                                                    'laptop\nCPU: i7-12700H\nRAM: 16G\n为基准的设备上迭代15s左右达到较好效果',
                                                    QLineEdit.Normal, '')
        # 判断有没有设置time
        if not okPressed:
            # 如果没有，pass
            pass
        else:
            try:
                # 如果进行了设置，重置self.time
                self.time = int(self.time)
                # 判断时间是不是大于0，否则恢复默认值并弹出异常
                if 0 >= self.time >= 50:
                    self.time = 15
                    self.error_act()
            except:
                self.error_act()

    def get_path_c(self, name):
        """点击按钮后选择content的路径，并把content和它的地址放到相应位置展示"""
        try:
            # 点击按钮后弹出文件选择框，并限制文件类型
            self.address_content_img_, pressed = QFileDialog.getOpenFileName(self,
                                                                             "choose a content img",
                                                                             "./",
                                                                             "图片(*.png *.jpg)")
            if pressed != '':
                # 把地址和图片放到对应的位置，并显示其地址
                self.address_content_img.setPlainText(self.address_content_img_.replace('/', '\\'))
                self.content = QtGui.QPixmap(self.address_content_img_)
                self.content_img.setPixmap(self.content)
            else:
                # 如果取消选择，把原来的图片放回来
                self.content_img.setPixmap(QtGui.QPixmap('./ph/C.png'))
                self.address_content_img.setPlainText('')

        except:
            self.error_act()

    def get_path_s(self):
        """点击按钮后选择style的路径，并把style和它的地址放到相应位置展示"""
        try:
            # 点击按钮后弹出文件选择框，并限制文件类型
            self.address_style_img_, pressed = QFileDialog.getOpenFileName(self,
                                                                           "choose a style img",
                                                                           "./",
                                                                           "图片(*.png *.jpg)")
            if pressed != '':
                # 把地址和图片放到对应的位置，并显示其地址
                self.address_style_img.setPlainText(self.address_style_img_.replace('/', '\\'))
                self.style = QtGui.QPixmap(self.address_style_img_)
                self.style_img.setPixmap(self.style)
            else:
                # 如果取消选择，把原来的图片放回来
                self.style_img.setPixmap(QtGui.QPixmap('./ph/S.png'))
                self.address_style_img.setPlainText('')
        except:
            self.error_act()

    def get_save_path(self):
        """获取保存路径"""
        try:
            # 使用getSaveFileName方法获取保存路径，并把过滤字符串丢弃
            path, _ = QFileDialog.getSaveFileName(self, "选择保存路径", './result.png', '图片(*.png)')
            return path

        except:
            self.error_act()

    def clear_logs(self):
        """清除logs日志"""
        """打开logs日志使用：tensorboard --logdir=logs"""
        # 判断是否存在该路径文件加
        path = os.path.exists('./logs')
        if not path:
            # 如果不存在创建一个
            os.makedirs('./logs')
        else:
            # 如果存在，使用os.chmod修改其权限（stat.S_IWRITE取消只读）
            os.chmod('./logs', stat.S_IWRITE)
            # 递归删除文件夹下的所有子文件夹和子文件
            shutil.rmtree('./logs')
            # 再重新创建一个日文件夹
            os.makedirs('./logs')
        self.clear_box.show()

    def error_act(self):
        """异常响应"""
        # 展示异常响应的窗体
        self.error_box.show()


if __name__ == '__main__':
    # 启动并保持你的应用程序的主事件循环
    app = QApplication([])
    # 设置整体风格
    app.setStyle("Fusion")
    # 手动添加动态链接库，防止jpg图片不能正常显示
    app.addLibraryPath(os.path.join(os.path.dirname(QtCore.__file__), "plugins"))
    # 创建窗体对象并显示
    window = Stats()
    window.show()
    # 启动循环
    app.exec()