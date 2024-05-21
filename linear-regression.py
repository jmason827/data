import torch
import torch.nn as nn
import numpy as np
from sklearn import datasets as skd
import matplotlib.pyplot as plt

# 1) design model
# 2) construct loss and optimizer
# 3) training loop
#   - forward pass: compute prediction and loss
#   - backward pass: gradients
#   - update weights

# generating some data
x_np, y_np = skd.make_regression(n_samples=20, n_features=1, noise=20, random_state=1)
# looks like x is a column vector
x = torch.from_numpy(x_np.astype(np.float32))
# while y is a row vector
y = torch.from_numpy(y_np.astype(np.float32))
# so we need to turn y into a column vector
# below we use the number of y's samples as the number of rows
y = y.view(y.shape[0], 1)

# we have 20 samples and one feature,
# where a 'feature' is a random variable
n_samples, n_features = x.shape

# 1) defining model
input_size = n_features
# we're predicting the value of a single dependent variable
output_size = 1
# the Linear() constructor takes the number of regressors
# and the number of regressands (response variables)
model = nn.Linear(input_size, output_size, bias=False)

# 2) loss and optimizer
learning_rate = 0.01
# our loss is the mean squared error
#   E[ (yp - yi)^2 ]
criterion = nn.MSELoss()
# stochastic gradient descent:
#   w := w - lr * grad( Qi(w) )
# looks to me that nn.Linear(ip,op).parameters() has two components:
#   w
#   b (additive bias)
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

# 3) training loop
num_epochs = 100
for epoch in range(num_epochs):
    # forward pass and loss
    # recall, x is a column vector 20 rows tall
    # so that y_predicted is a 20-row response vector
    y_predicted = model(x)
    # we converted y to a column vector, so this here is
    #   mean( (yp - y)^2 )
    # and loss is scalar
    loss = criterion(y_predicted, y)
    # backward pass (gradient calc?)
    loss.backward()
    # update (using the gradients calculated from backward?)
    optimizer.step()
    # empty the gradients for next update step
    optimizer.zero_grad()

    if (epoch+1) % 10 == 0:
        print(f"epoch: {epoch+1}, loss = {loss.item():.4f}")

# plot
predicted = model(x).detach().numpy()
plt.plot(x_np, y_np, 'ro')
plt.plot(x_np, predicted, 'b')
plt.show()
