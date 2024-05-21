import os
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

w0 = 0.125
b0 = 5.0
x_range = [-20, 60]

def load_dataset(n=150, n_tst=150):
    np.random.seed(43)

    def s(x):
        g = (x - x_range[0]) / (x_range[1] - x_range[0])
        return 3 * (0.25 + g**2.0)
    
    x = (x_range[1] - x_range[0]) * np.random.rand(n) + x_range[0]
    eps = np.random.randn(n) * s(x)
    y = (w0 * x * (1.0 + np.sin(x)) + b0) + eps
    x = x[..., np.newaxis]
    x_tst = np.linspace(*x_range, num=n_tst).astype(np.float32)
    return y, x, x_tst

y, x, x_tst = load_dataset()

plt.figure()
plt.plot(x, y, "b.", label="observed")
plt.show()

# look like the example code (tf) stacks two layers in the model
#   1) linear dot product
#   2) gaussian distribution
# to do this in torch, I think we need to use 
#   torch.nn.GaussianNLLLoss(*, full=False, eps=1e-06, reduction='mean')
# that's an nn.Linear layer plus a gaussian loss layer (neg log lik)
