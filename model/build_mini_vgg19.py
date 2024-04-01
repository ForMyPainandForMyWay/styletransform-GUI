import vgg19
from torch import nn
from torch import load
from torch import save

VGG19 = vgg19.VGG19()
pre_file = load(r".\vgg19.pth")
VGG19.load_state_dict(pre_file)

mini_vgg19 = nn.Module()
_ = nn.Sequential()

i = 0
for name, layer in VGG19.named_modules():
    if i <= 11:
        if isinstance(layer, nn.Conv2d):
            _.add_module(name=str(i), module=layer)
            i += 1
        elif isinstance(layer, nn.MaxPool2d):
            _.add_module(name=str(i), module=layer)
            i += 1
        elif isinstance(layer, nn.ReLU):
            _.add_module(name=str(i), module=layer)
            i += 1
    else:
        break

mini_vgg19.add_module(name='model', module=_)
print(mini_vgg19)
save(mini_vgg19.state_dict(), "mini_vgg19.pth")
