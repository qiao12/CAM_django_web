import torch
a = torch.load('/home/hp/PycharmProjects/CAM/model_best.pth')
torch.save(a,'model_best.t7')