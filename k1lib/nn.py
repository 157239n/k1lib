# AUTOGENERATED FILE! PLEASE DON'T EDIT
import torch.nn as _nn
class Lambda(_nn.Module):
    def __init__(self, f): super().__init__(); self.f = f
    def forward(self, x): return self.f(x)